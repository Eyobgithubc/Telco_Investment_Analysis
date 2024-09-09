def aggregate_scores_per_cluster(df):
    """
    Aggregate the average satisfaction and experience scores per cluster.

    Parameters:
    df (pd.DataFrame): DataFrame containing 'satisfaction_score', 'experience_score', and 'cluster'.

    Returns:
    pd.DataFrame: Aggregated average scores per cluster.
    """
    # Aggregate average satisfaction and experience scores per cluster
    cluster_averages = df.groupby('cluster').agg({
        'satisfaction_score': 'mean',
        'experience_score': 'mean'
    }).reset_index()

    # Print the aggregated averages
    print("\nAverage Satisfaction & Experience Scores per Cluster:")
    print(cluster_averages)

    # Return the aggregated DataFrame
    return cluster_averages


