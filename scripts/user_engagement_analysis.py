import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

def aggregate_and_report_top_customers(df):
   
    df_agg = df.groupby('MSISDN/Number').agg({
        'Dur. (ms)': 'count',  
        'Activity Duration DL (ms)': 'sum',  
        'Total DL (Bytes)': 'sum',  
        'Total UL (Bytes)': 'sum'   
    }).reset_index()
    
    
    df_agg['Total Traffic (Bytes)'] = df_agg['Total DL (Bytes)'] + df_agg['Total UL (Bytes)']
    
    
    top_sessions = df_agg.nlargest(10, 'Dur. (ms)')
    top_duration = df_agg.nlargest(10, 'Activity Duration DL (ms)')
    top_traffic = df_agg.nlargest(10, 'Total Traffic (Bytes)')
    
    return top_sessions, top_duration, top_traffic



def cluster_and_analyze_engagement(df):
   
    df['Total Traffic (Bytes)'] = df['Total DL (Bytes)'] + df['Total UL (Bytes)']
    
   
    metrics = df[['Dur. (ms)', 'Activity Duration DL (ms)', 'Total Traffic (Bytes)']]
    scaler = StandardScaler()
    metrics_scaled = scaler.fit_transform(metrics)
    
   
    kmeans = KMeans(n_clusters=3, random_state=0)
    df['Cluster'] = kmeans.fit_predict(metrics_scaled)
    
   
    cluster_summary = df.groupby('Cluster').agg({
        'Dur. (ms)': ['min', 'max', 'mean', 'sum'],
        'Activity Duration DL (ms)': ['min', 'max', 'mean', 'sum'],
        'Total Traffic (Bytes)': ['min', 'max', 'mean', 'sum']
    }).reset_index()
    
    return df, cluster_summary




def aggregate_user_traffic(df):
   
    applications = [
        'Social Media DL (Bytes)', 'Google DL (Bytes)', 'Email DL (Bytes)',
        'Youtube DL (Bytes)', 'Netflix DL (Bytes)', 'Gaming DL (Bytes)',
        'Other DL (Bytes)'
    ]
    
    
    results = {}
    
    for app in applications:
        
        traffic_per_user = df.groupby('MSISDN/Number')[app].sum().reset_index()
        traffic_per_user = traffic_per_user.rename(columns={app: 'Total Traffic (Bytes)'})
        
        
        top_users = traffic_per_user.sort_values(by='Total Traffic (Bytes)', ascending=False).head(10)
        
        results[app] = top_users
    
    
    result_df = pd.concat(results, axis=1)
    return result_df

def plot_top_applications(df):
   
    app_totals = df[['Social Media DL (Bytes)', 'Google DL (Bytes)', 'Email DL (Bytes)',
                     'Youtube DL (Bytes)', 'Netflix DL (Bytes)', 'Gaming DL (Bytes)', 
                     'Other DL (Bytes)']].sum().sort_values(ascending=False)
    
    top_3_apps = app_totals.head(3)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_3_apps.index, y=top_3_apps.values)
    plt.title('Top 3 Most Used Applications')
    plt.xlabel('Application')
    plt.ylabel('Total Download (Bytes)')
    plt.show()



