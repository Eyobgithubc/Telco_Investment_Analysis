import pandas as pd


def analyze_data(df):
    
    required_columns = ['Total Sessions', 'Total Duration (ms)', 'Total Download (Bytes)', 'Total Upload (Bytes)']
    
    if not all(col in df.columns for col in required_columns):
        raise ValueError("Required columns are missing from the dataframe")

   
    df['total_data'] = df['Total Download (Bytes)'] + df['Total Upload (Bytes)']

    
    df['decile'] = pd.qcut(df['Total Duration (ms)'], 10, labels=False, duplicates='drop')

    
    decile_summary = df.groupby('decile')['total_data'].sum().reset_index()
    
    
    decile_summary['Total Sessions'] = df.groupby('decile')['Total Sessions'].sum().reset_index()['Total Sessions']
    decile_summary['Total Duration (ms)'] = df.groupby('decile')['Total Duration (ms)'].mean().reset_index()['Total Duration (ms)']
    decile_summary['average_data_per_session'] = decile_summary['total_data'] / decile_summary['Total Sessions']

    return decile_summary










def non_graphical_univariate_analysis(df, numeric_columns):
   
    results = []

    for col in numeric_columns:
        mean_value = df[col].mean()
        median_value = df[col].median()
        std_dev_value = df[col].std()
       
        results.append({
            'Column': col,
            'Mean': mean_value,
            'Median': median_value,
            'Std Dev': std_dev_value
        })

    results_df = pd.DataFrame(results)
    
    return results_df

import matplotlib.pyplot as plt
import seaborn as sns

def plot_univariate_analysis(df, column_name):
   
    
    if column_name in df.columns:
        plt.figure(figsize=(12, 6))
        
        plt.subplot(1, 2, 1)
        sns.histplot(df[column_name], kde=True, bins=30)
        plt.title(f'{column_name} Distribution')
        plt.xlabel(column_name)
       
        plt.subplot(1, 2, 2)
        sns.boxplot(x=df[column_name])
        plt.title(f'{column_name} Boxplot')
        plt.xlabel(column_name)
       
        plt.tight_layout()
        plt.show()
    else:
        print(f"Column '{column_name}' not found in the DataFrame.")


import matplotlib.pyplot as plt
import seaborn as sns

def generate_scatter_plots(df, app_columns, total_data_col):
    """
    Generates scatter plots for each application-specific column against total data usage.

    Parameters:
    - df: The DataFrame containing the data.
    - app_columns: A list of application-specific columns.
    - total_data_col: The column representing total data usage.

    Returns:
    - None (displays scatter plots).
    """
    import matplotlib.pyplot as plt
    import seaborn as sns

    plt.figure(figsize=(16, 10))
    
    for i, app_col in enumerate(app_columns, start=1):
        plt.subplot(2, 3, i)
        sns.scatterplot(x=df[app_col], y=df[total_data_col])
        plt.title(f"{app_col} vs {total_data_col}")
        plt.xlabel(app_col)
        plt.ylabel(total_data_col)
    
    plt.tight_layout()
    plt.show()

def generate_box_plots(df, app_columns, total_data_col):
  
    import matplotlib.pyplot as plt
    import seaborn as sns

    plt.figure(figsize=(16, 10))
    
    for i, app_col in enumerate(app_columns, start=1):
        plt.subplot(2, 3, i)
        sns.boxplot(x=df[app_col], y=df[total_data_col])
        plt.title(f"{app_col} vs {total_data_col}")
        plt.xlabel(app_col)
        plt.ylabel(total_data_col)
    
    plt.tight_layout()
    plt.show()

def correlation_heatmap(df, app_columns, total_data_col):
    """
    Generates a heatmap of correlations between application-specific columns and total data usage.

    Parameters:
    - df: The DataFrame containing the data.
    - app_columns: A list of application-specific columns.
    - total_data_col: The column representing total data usage.

    Returns:
    - None (displays the correlation heatmap).
    """
    import seaborn as sns
    import matplotlib.pyplot as plt

    # Select the columns for correlation analysis
    columns = app_columns + [total_data_col]
    correlation_matrix = df[columns].corr()

    # Plot heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
    plt.title('Correlation Heatmap')
    plt.show()



def correlation_analysis(df, app_columns):
   
    
    correlation_matrix = df[app_columns].corr()

    
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
    plt.title('Application Data Usage Correlation Matrix')
    plt.show()

    
    print("Correlation Matrix:")
    print(correlation_matrix)


app_columns = [
    'Social Media Download (Bytes)', 'Google Download (Bytes)', 'Email Download (Bytes)', 
    'YouTube Download (Bytes)', 'Netflix Download (Bytes)', 'Gaming Download (Bytes)'
]



from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import pandas as pd
import matplotlib.pyplot as plt

def perform_pca(df, features, n_components=2):
   
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df[features])

    
    pca = PCA(n_components=n_components)
    principal_components = pca.fit_transform(scaled_data)
    
    
    pca_df = pd.DataFrame(data=principal_components, 
                          columns=[f'PC{i+1}' for i in range(n_components)])
    
    plt.figure(figsize=(8, 6))
    plt.bar(range(1, n_components + 1), pca.explained_variance_ratio_, color='skyblue')
    plt.title('Explained Variance by Principal Components')
    plt.xlabel('Principal Component')
    plt.ylabel('Variance Explained')
    plt.show()
    
    explained_variance = pca.explained_variance_ratio_
    print(f"Explained Variance Ratio: {explained_variance}")
    
    return pca_df, explained_variance






