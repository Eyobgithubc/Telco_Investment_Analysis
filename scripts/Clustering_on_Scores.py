from sklearn.cluster import KMeans
import pandas as pd
import numpy as np

# Assuming df is your DataFrame and engagement and experience features have been defined
# Run K-means on the engagement and experience scores

def run_kmeans_on_scores(df):
    # Extracting engagement and experience features
    engagement_data = df['engagement_score'].values.reshape(-1, 1)
    experience_data = df['experience_score'].values.reshape(-1, 1)

    # Combine engagement and experience scores into one array
    scores_data = np.hstack((engagement_data, experience_data))

    # Perform K-means clustering with k=2
    kmeans = KMeans(n_clusters=2, random_state=42)
    clusters = kmeans.fit_predict(scores_data)

    # Assign clusters back to the DataFrame
    df['cluster'] = clusters

    # Print cluster centroids
    print("Cluster centroids:")
    print(kmeans.cluster_centers_)

    # Return the updated DataFrame
    return df

# Example usage:
# updated_df = run_kmeans_on_scores(df)
