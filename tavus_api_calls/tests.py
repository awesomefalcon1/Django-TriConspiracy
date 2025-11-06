from django.test import TestCase

from django.test import Client, TestCase
from django.urls import reverse
from main.engines import ContentEngine, LargeFeatureExtractionEngine, GGUFContentEngine
from main.constants import settings
import json
import pandas as pd
import tempfile
import os

class RecommendationServiceTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.headers = {'HTTP_X_API_TOKEN': settings.Constants.API_TOKEN}

    def test_predict_endpoint(self):
        response = self.client.post(reverse('predict'), 
                                    {'item': '1', 'num': 5},
                                    **self.headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 5)
        for item in data:
            self.assertIsInstance(item, list)
            self.assertEqual(len(item), 2)
            self.assertIsInstance(item[0], str)
            self.assertIsInstance(item[1], float)

    def test_train_endpoint(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as temp_file:
            temp_file.write("id,description\n1,test product\n2,another product")
            temp_file.flush()
            
            response = self.client.post(reverse('train'),
                                        {'data-url': temp_file.name},
                                        **self.headers)
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.content)
            self.assertEqual(data['success'], 1)
            self.assertEqual(data['message'], 'Success!')
        
        os.unlink(temp_file.name)

    def test_feature_extraction(self):
        response = self.client.post(reverse('feature_extraction'),
                                    {'text': 'test sentence'},
                                    **self.headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('embedding', data)
        self.assertIsInstance(data['embedding'], list)

    def test_sentence_similarity(self):
        response = self.client.post(reverse('sentence_similarity'),
                                    {'text1': 'hello world', 'text2': 'hello there'},
                                    **self.headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('similarity', data)
        self.assertIsInstance(data['similarity'], float)
        self.assertGreaterEqual(data['similarity'], 0)
        self.assertLessEqual(data['similarity'], 1)

    def test_large_feature_extraction(self):
        response = self.client.post(reverse('fetch_large_feature_extraction_engine'),
                                    {'model-name': 'sentence-transformers/all-MiniLM-L6-v2'},
                                    **self.headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['success'], 1)
        self.assertEqual(data['loaded_model'], 'sentence-transformers/all-MiniLM-L6-v2')

    def test_extract_features_with_large_feature_extraction_engine(self):
        # First load the model
        self.client.post(reverse('fetch_large_feature_extraction_engine'),
                         {'model-name': 'sentence-transformers/all-MiniLM-L6-v2'},
                         **self.headers)
        
        response = self.client.post(reverse('extract_features_with_large_feature_extraction_engine'),
                                    {'text': 'test sentence'},
                                    **self.headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('embedding', data)
        self.assertIsInstance(data['embedding'], list)

    def test_sentence_similarity_with_large_feature_extraction_engine(self):
        # First load the model
        self.client.post(reverse('fetch_large_feature_extraction_engine'),
                         {'model-name': 'sentence-transformers/all-MiniLM-L6-v2'},
                         **self.headers)
        
        response = self.client.post(reverse('sentence_similarity_with_large_feature_extraction_engine'),
                                    {'text1': 'hello world', 'text2': 'hello there'},
                                    **self.headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('similarity', data)
        self.assertIsInstance(data['similarity'], float)
        self.assertGreaterEqual(data['similarity'], 0)
        self.assertLessEqual(data['similarity'], 1)

    def test_GGUF_engine_feature_extraction(self):
        # First load the model
        response = self.client.post(reverse('fetch_GGUF_embeddings_model'),
                                    {'model-name': 'test-model'},
                                    **self.headers)
        self.assertEqual(response.status_code, 200)
        
        # Then test feature extraction
        response = self.client.post(reverse('extract_features_with_GGUF_engine'),
                                    {'text': 'test sentence'},
                                    **self.headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('embedding', data)
        self.assertIsInstance(data['embedding'], list)

    def test_GGUF_engine_sentence_similarity(self):
        # First load the model
        self.client.post(reverse('fetch_GGUF_embeddings_model'),
                         {'model-name': 'test-model'},
                         **self.headers)
        
        response = self.client.post(reverse('sentence_similarity_with_GGUF_engine'),
                                    {'text1': 'hello world', 'text2': 'hello there'},
                                    **self.headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('similarity', data)
        self.assertIsInstance(data['similarity'], float)
        self.assertGreaterEqual(data['similarity'], 0)
        self.assertLessEqual(data['similarity'], 1)

    def test_unauthorized_access(self):
        response = self.client.post(reverse('predict'),
                                    {'item': '1', 'num': 5})
        self.assertEqual(response.status_code, 403)

    def test_train_ui(self):
        response = self.client.get(reverse('train_ui'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'train.html')

        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as temp_file:
            temp_file.write("id,description\n1,test product\n2,another product")
            temp_file.flush()
            
            response = self.client.post(reverse('train_ui'),
                                        {'data-url': temp_file.name})
            self.assertEqual(response.status_code, 302)  # Redirect after successful training
            self.assertRedirects(response, reverse('train_ui'))
        
        os.unlink(temp_file.name)

