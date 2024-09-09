import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import euclidean_distances
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sqlalchemy import create_engine
import logging
import time


def calculate_scores(data, centroids, cluster_idx):
    
    return euclidean_distances(data, centroids[cluster_idx].reshape(1, -1)).flatten()


def assign_engagement_experience_scores(df, engagement_features, experience_features):
   
    engagement_data = df[engagement_features].fillna(0)
    experience_data = df[experience_features].fillna(0)

    
    kmeans_engagement = KMeans(n_clusters=2)
    engagement_clusters = kmeans_engagement.fit_predict(engagement_data)
    
    kmeans_experience = KMeans(n_clusters=2)
    experience_clusters = kmeans_experience.fit_predict(experience_data)

   
    engagement_centroids = kmeans_engagement.cluster_centers_
    experience_centroids = kmeans_experience.cluster_centers_

    df['engagement_score'] = calculate_scores(engagement_data, engagement_centroids, 0)
    df['experience_score'] = calculate_scores(experience_data, experience_centroids, 1)
    

    df['satisfaction_score'] = (df['engagement_score'] + df['experience_score']) / 2
    
    return df