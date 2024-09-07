import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns



def aggregate_per_customer(data):
    
    numeric_cols = data.select_dtypes(include=['float64', 'int64']).columns
    non_numeric_cols = ['Handset Type']  
    
  
    mean_tcp_dl_retrans = data.loc[data['TCP DL Retrans. Vol (Bytes)'] != 0, 'TCP DL Retrans. Vol (Bytes)'].mean()
    data['TCP DL Retrans. Vol (Bytes)'] = data['TCP DL Retrans. Vol (Bytes)'].replace(0, mean_tcp_dl_retrans)
    
    
    mean_imputer = SimpleImputer(strategy='mean')
    data[numeric_cols] = mean_imputer.fit_transform(data[numeric_cols])
    
   
    mode_imputer = SimpleImputer(strategy='most_frequent')
    data[non_numeric_cols] = mode_imputer.fit_transform(data[non_numeric_cols])
    
   
    agg_data = data.groupby(['IMSI', 'Handset Type']).agg({
        'TCP DL Retrans. Vol (Bytes)': 'mean',
        'TCP UL Retrans. Vol (Bytes)': 'mean',
        'Avg RTT DL (ms)': 'mean',
        'Avg RTT UL (ms)': 'mean',
        'Avg Bearer TP DL (kbps)': 'mean',
        'Avg Bearer TP UL (kbps)': 'mean'
    }).reset_index()

    
    agg_data['Avg TCP Retransmission'] = (agg_data['TCP DL Retrans. Vol (Bytes)'] + agg_data['TCP UL Retrans. Vol (Bytes)']) / 2
    agg_data['Avg RTT'] = (agg_data['Avg RTT DL (ms)'] + agg_data['Avg RTT UL (ms)']) / 2
    agg_data['Avg Throughput'] = (agg_data['Avg Bearer TP DL (kbps)'] + agg_data['Avg Bearer TP UL (kbps)']) / 2
    
    return agg_data







def top_bottom_most_frequent(agg_data, column):
    top_10 = agg_data[column].nlargest(10)
    bottom_10 = agg_data[column].nsmallest(10)
    most_frequent = agg_data[column].value_counts().nlargest(10)
    return top_10, bottom_10, most_frequent


def compute_distributions(agg_data):
    throughput_per_handset = agg_data.groupby('Handset Type')['Avg Throughput'].mean().sort_values()
    tcp_per_handset = agg_data.groupby('Handset Type')['Avg TCP Retransmission'].mean().sort_values()
    
    
    plt.figure(figsize=(10, 6))
    sns.histplot(throughput_per_handset, bins=20, kde=True)
    plt.title('Distribution of Average Throughput Per Handset Type')
    plt.show()
    
    plt.figure(figsize=(10, 6))
    sns.histplot(tcp_per_handset, bins=20, kde=True)
    plt.title('Average TCP Retransmission Per Handset Type')
    plt.show()

    return throughput_per_handset, tcp_per_handset


def kmeans_clustering(agg_data):
    
    features = ['Avg TCP Retransmission', 'Avg RTT', 'Avg Throughput']
    X = agg_data[features]
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    kmeans = KMeans(n_clusters=3, random_state=0)
    agg_data['Cluster'] = kmeans.fit_predict(X_scaled)
    
    cluster_centers = scaler.inverse_transform(kmeans.cluster_centers_)
    cluster_centers_df = pd.DataFrame(cluster_centers, columns=features)
    
    cluster_descriptions = []
    for i in range(3):
        description = (f"Cluster {i}: "
                       f"Avg TCP Retransmission: {cluster_centers_df.loc[i, 'Avg TCP Retransmission']:.2f}, "
                       f"Avg RTT: {cluster_centers_df.loc[i, 'Avg RTT']:.2f} ms, "
                       f"Avg Throughput: {cluster_centers_df.loc[i, 'Avg Throughput']:.2f} kbps")
        cluster_descriptions.append(description)
    
    return agg_data, cluster_descriptions

