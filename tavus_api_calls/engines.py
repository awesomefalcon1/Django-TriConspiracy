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