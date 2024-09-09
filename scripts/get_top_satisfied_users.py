def get_top_satisfied_customers(df, top_n=10):
    
    
    if 'satisfaction_score' not in df.columns:
        raise ValueError("The DataFrame does not contain 'satisfaction_score' column. Please run 'assign_engagement_experience_scores' first.")

    sorted_df = df.sort_values(by='satisfaction_score', ascending=False)
    

    top_customers = sorted_df.head(top_n)
    
    return top_customers