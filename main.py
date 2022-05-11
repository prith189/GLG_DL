# -*- coding: utf-8 -*-
"""Clustering.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1hSxFUAsvlgOOdJP0nmf_IIWe1HCZ9qv5
"""



"""Pipeline suggested by BERTopic:

- Generate embeddings using the Sentence Transformer model (Each block of text is converted to a 384 dimensional vector)

- Reduce the dimensionality using UMAP for 384 dimensions to 5 dimensions

- Cluster the 5 dimensional vectors using HDBSCAN

- For each cluster, run TF-IDF to generate a representation of the topic


Changes made to use the News dataset

- For clustering, HDBSCAN classifies most of the vectors in the embedded space as noise

- Kmeans clusters all data points into clusters, therefore KMeans was used

- In the below notebook, UMAP was used for dimensionality reduction and Kmeans was used for clustering
"""

# RUN_SENTENCE_TRANSFORMER = False #Set this to True if we need to generate embeddings from scratch. Requires GPU else very slow.
# RUN_UMAP = False #Set this to True if we need to reduce the dimensionality of the embeddings using UMAP (Requires >100GB of RAM to run for all data points)
# RUN_KMEANS = False #Set this to True if we need to run KMeans on the reduce dimension vectors
# EXTRACT_TOPICS = False #Set this to True to extract a description of each of the topics
# LABEL_TOPICS = False
# TEST_NEW_TEXT = True #To test out new topics

# !pip install umap-learn

# !pip install transformers[sentencepiece] sentence-transformers

# use_drive = True

# if(use_drive):
#     from google.colab import drive
#     drive.mount('/content/drive', force_remount=True)
#     BASE_PATH = '/content/drive/My Drive/fourthbrain/'
# else:
#     BASE_PATH = '/content/'

BASE_PATH = './'

#EMBEDDINGS FILE
#!wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1-3gKYoipfdPkeQHnHa0M2vD7QEug5wNS' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1-3gKYoipfdPkeQHnHa0M2vD7QEug5wNS" -O all-the-news-embeddings-title.npy && rm -rf /tmp/cookies.txt

#INDEX FILE for NEWS DATASET (so that the embeddings file matches the entries from the news.csv file)
#!wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1-5IsScXPtUY5jXVe_83RuQ0uI7eQqDMI' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1-5IsScXPtUY5jXVe_83RuQ0uI7eQqDMI" -O all-the-news-embeddings-title-index.npy && rm -rf /tmp/cookies.txt

#!wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1Cr0YuS85hynqfi_4_Kr99h4HTTUpsZ-u' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1Cr0YuS85hynqfi_4_Kr99h4HTTUpsZ-u" -O all-the-news-2-1.csv && rm -rf /tmp/cookies.txt

from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np
import pickle
import os
import joblib

csv_file = 'all-the-news-2-1.csv'

class FeatureExtraction:
    def __init__(self):
        #Load the pretrained model
        self.fe = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

    def run_fe_batch(self, list_of_input_text):
        list_of_fe_vec = self.fe.encode(list_of_input_text, show_progress_bar=False)
        return list_of_fe_vec


class NewsDataset:
    def __init__(self):
        self.df = pd.read_csv(csv_file)
        self.preprocess()
        self.ner = None
    
    def preprocess(self):
        self.df.drop(columns=['Unnamed: 0', 'Unnamed: 0.1','date','year','month','day','article','publication'], inplace=True)
        print('Shape of dataframe before dropping nan:{}'.format(self.df.shape))
        self.df = self.df.dropna(subset=['title'])
        print('Shape of dataframe after dropping nan:{}'.format(self.df.shape))


class Prediction:
    def __init__(self):
        
        #Load the embeddings
        print('Loading embeddings')
        features_file = os.path.join(BASE_PATH, 'all-the-news-embeddings-title.npy')
        idx_file = os.path.join(BASE_PATH, 'all-the-news-embeddings-title-index.npy')
        self.features = np.load(features_file)
        self.df_idx = np.load(idx_file)
        
        #Download link for features_file
        #!wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1-3gKYoipfdPkeQHnHa0M2vD7QEug5wNS' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1-3gKYoipfdPkeQHnHa0M2vD7QEug5wNS" -O all-the-news-embeddings-title.npy && rm -rf /tmp/cookies.txt
        
        #Download link for idx_file
        #!wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1-5IsScXPtUY5jXVe_83RuQ0uI7eQqDMI' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1-5IsScXPtUY5jXVe_83RuQ0uI7eQqDMI" -O all-the-news-embeddings-title-index.npy && rm -rf /tmp/cookies.txt
        
        
        
        print('Loading Dimensionality reduction model')
        #Load the dimensionality reduction model
        dim_red_embeddings_file = os.path.join(BASE_PATH, 'all-the-news-embeddings-title-umap.npy')
        umap_model_file = os.path.join(BASE_PATH, 'umap-model.sav')
        self.dim_red_embeddings = np.load(dim_red_embeddings_file)
        self.umap_model = joblib.load(umap_model_file)
        
        #Download link for dim_red_embeddings
        #!wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1OieSf2kPtyTYuTiYJSTsNa7jpCsaQnum' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1OieSf2kPtyTYuTiYJSTsNa7jpCsaQnum" -O all-the-news-embeddings-title-umap.npy && rm -rf /tmp/cookies.txt
        
        #Download link for umap_model_file
        #!wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1ibBI4BMS6zKfjPWarxdNKNvOuIt5Mj2D' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1ibBI4BMS6zKfjPWarxdNKNvOuIt5Mj2D" -O umap-model.sav && rm -rf /tmp/cookies.txt
        
        print('Clustering model')
        #Load the Clustering model
        kmeans_model_file = os.path.join(BASE_PATH, 'kmeans_model.p')
        labels_file = os.path.join(BASE_PATH, 'umap-kmeans-labels.npy')
        f = open(kmeans_model_file, 'rb')
        self.kmn = pickle.load(f)
        f.close()
        self.labels = np.load(labels_file)
        
        #Download link for kmeans_model
        #!wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1qBL6k2w06IbXs1h_tNJb52QW6gkKhBGy' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1qBL6k2w06IbXs1h_tNJb52QW6gkKhBGy" -O kmeans_model.p && rm -rf /tmp/cookies.txt
        
        #Download link for labels_file
        #!wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1bNF2rhe2rdG7zzPoay_NziXAjLtwLXhg' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1bNF2rhe2rdG7zzPoay_NziXAjLtwLXhg" -O umap-kmeans-labels.npy && rm -rf /tmp/cookies.txt
        
        
        print('Loading the topics file')
        #Load the topics file
        topics_file = os.path.join(BASE_PATH, 'umap-kmeans-topics.p')
        f = open(topics_file, 'rb')
        self.topics = pickle.load(f)
        f.close()
        
        #Download link for topics_file
        #!wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1-1LXRgomfpqloQEvbDgfR_Hx7SAnOfWD' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1-1LXRgomfpqloQEvbDgfR_Hx7SAnOfWD" -O umap-kmeans-topics.p && rm -rf /tmp/cookies.txt
        
        
        
        print('Loading the topic labels file')
        #Load the topic labels file
        topic_labels_file = os.path.join(BASE_PATH, 'umap-kmeans-topic-labels.p')
        f = open(topic_labels_file, 'rb')
        self.topic_labels = pickle.load(f)
        f.close()
        
        
        #Download link for topic_labels_file
        #!wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1-3p3vZYdY8iytnDn5gUaUVcabKfkrUhq' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1-3p3vZYdY8iytnDn5gUaUVcabKfkrUhq" -O umap-kmeans-topic-labels.p && rm -rf /tmp/cookies.txt
        
        
        print('Initializing the feature extractor')
        self.feature_extractor = FeatureExtraction()
        
    def run_prediction(self, new_text):
        test_embeddings = self.feature_extractor.run_fe_batch(new_text)
        test_dim_red_embeddings = self.umap_model.transform(test_embeddings)
        test_labels = list(self.kmn.predict(test_dim_red_embeddings))
        for label, text in zip(test_labels, new_text):
            print('Test text:', text)
            print('Predicted Topic:', self.topic_labels[label])
            print('Predicted keywords:', '_'.join([i[0] for i in self.topics[label][:5]]))
            print('*****************************')

if __name__=="__main__":
    predictor = Prediction()
    st = []
    st.append('Secret Service on the defensive over allegations agents were duped by men impersonating feds') #Government
    st.append('Microsoft and other tech firms take aim at prolific cybercrime gang') #Technology
    st.append('Phoenix Suns favorites to win NBA title, but they still feel disrespected. Are they overlooked?') #Sports
    st.append("Natural gas spikes to highest level since 2008 as rare nor'easter looms") #Business
    st.append("Will rising prices sink Biden’s midterm hopes for Democrats?") #Politics
    st.append("Large and dangerous' tornadoes hit Texas and Oklahoma; South faces more severe weather") #Climate
    st.append("Here is a list of the best beaches in Hawaii and other tropical islands") #Travel
    predictor.run_prediction()