import pandas as pd
import time
import redis
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from main.constants import Constants
import torch
from transformers import AutoTokenizer, AutoModel
from llama_cpp import Llama

def info(msg):
    import logging
    logger = logging.getLogger(__name__)
    logger.info(msg)

class ContentEngine(object):

    SIMKEY = 'p:smlr:%s'

    def __init__(self):
        self._r = redis.StrictRedis.from_url(Constants.REDIS_URL)

    def train(self, data_source):
        start = time.time()
        ds = pd.read_csv(data_source)
        info("Training data ingested in %s seconds." % (time.time() - start))

        # Flush the stale training data from redis
        self._r.flushdb()

        start = time.time()
        self._train(ds)
        info("Engine trained in %s seconds." % (time.time() - start))

    def _train(self, ds):
        """
        Train the engine.

        Create a TF-IDF matrix of unigrams, bigrams, and trigrams for each product. The 'stop_words' param
        tells the TF-IDF module to ignore common english words like 'the', etc.

        Then we compute similarity between all products using SciKit Leanr's linear_kernel (which in this case is
        equivalent to cosine similarity).

        Iterate through each item's similar items and store the 100 most-similar. Stops at 100 because well...
        how many similar products do you really need to show?

        Similarities and their scores are stored in redis as a Sorted Set, with one set for each item.

        :param ds: A pandas dataset containing two fields: description & id
        :return: Nothin!
        """
        tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0.01, stop_words='english')
        tfidf_matrix = tf.fit_transform(ds['description'])

        cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

        for idx, row in ds.iterrows():
            similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
            similar_items = [(cosine_similarities[idx][i], ds['id'][i]) for i in similar_indices]

            # First item is the item itself, so remove it.
            # Convert list of tuples to dict for zadd
            similar_dict = {str(item_id): float(score) for score, item_id in similar_items[1:]}
            self._r.zadd(self.SIMKEY % str(row['id']), similar_dict)

    def predict(self, item_id, num):
        """
        Couldn't be simpler! Just retrieves the similar items and their 'score' from redis.

        :param item_id: string
        :param num: number of similar items to return
        :return: A list of lists like: [["19", 0.2203], ["494", 0.1693], ...]. The first item in each sub-list is
        the item ID and the second is the similarity score. Sorted by similarity score, descending.
        """
        return self._r.zrange(self.SIMKEY % item_id, 0, num-1, withscores=True, desc=True)

    def feature_extraction(self, sentence):
        tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0.01, stop_words='english')
        tfidf_matrix = tf.fit_transform(sentence)
        return tfidf_matrix
    
    def sentence_similarity(self, sentence1, sentence2):
        tfidf_matrix1 = self.feature_extraction(sentence1)
        tfidf_matrix2 = self.feature_extraction(sentence2)
        cosine_similarities = linear_kernel(tfidf_matrix1, tfidf_matrix2)
        return cosine_similarities[0][0]
    

class LargeFeatureExtractionEngine(object):
    
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
    
    def set_model(self, model_name):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.model_name = model_name
    
    def extract_features(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        with torch.no_grad():
            outputs = self.model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).squeeze()
    
    def sentence_similarity(self, sentence1, sentence2):
        embeddings1 = self.extract_features(sentence1)
        embeddings2 = self.extract_features(sentence2)
        return embeddings1 @ embeddings2.T
    
    def score_matrix(self, csv_path, sentence_col):
        df = pd.read_csv(csv_path)
        
        embeddings = []
        score_matrix = []
        
        for _, row in df.iterrows():
            embedding = self.extract_features(row[sentence_col])
            embeddings.append(embedding)
            
        for i in range(len(embeddings)):
            score_matrix.append([])
            for j in range(len(embeddings)):
                score_matrix[i].append(embeddings[i] @ embeddings[j].T)
        
        return score_matrix
    
    def feature_extraction(self, csv_path, sentence_col):
        df = pd.read_csv(csv_path)
        embeddings = []
        for _, row in df.iterrows():
            embedding = self.extract_features(row[sentence_col])
            embeddings.append(embedding)
        return embeddings

class LLMContentEngine(object):
    
    def __init__(self, model_name='meta-llama/Meta-Llama-3-8B-Instruct'):
        self.model = model_name
    
    def set_model(self, model_name):
        self.model = model_name

class GGUFContentEngine(object):
    
    def __init__(self):
        self.chat_model = None
        self.embedding_model = None
    
    def set_embedding_model(self, model_path, filename):
        self.embedding_model = Llama.from_pretrained(
            repo_id = model_path,
            filename = filename,
            embedding = True,
            verbose = False)
    
    def set_chat_model(self, model_path, filename):
        self.chat_model = Llama.from_pretrained(
            repo_id = model_path,
            filename = filename,
            verbose = False)
    
    def chat_completion(self, prompt):
        pass
    
    def extract_features(self, text):
        embeddings = self.embedding_model.create_embedding(text)
        dimension_vector = torch.Tensor(embeddings['data'][0]['embedding'])
        return dimension_vector
    
    def sentence_similarity(self, sentence1, sentence2):
        embedding1 = self.extract_features(sentence1)
        embedding2 = self.extract_features(sentence2)
        return embedding1 @ embedding2.T

    def feature_extraction(self, csv_path, sentence_col):
        embeddings = []
        for _, row in pd.read_csv(csv_path).iterrows():
            embeddings.append(self.extract_features(row[sentence_col]))
        return embeddings

    def score_matrix(self, csv_path, sentence_col):
        embeddings = self.feature_extraction(csv_path, sentence_col)
        score_matrix = []
        for i in range(len(embeddings)):
            score_matrix.append([])
            for j in range(len(embeddings)):
                score_matrix[i].append(embeddings[i] @ embeddings[j].T)
        return score_matrix