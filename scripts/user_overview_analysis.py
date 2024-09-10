import pandas as pd

def identify_top_handsets(handsets_data):
   
    handset_counts = handsets_data['Handset Type'].value_counts().head(10)
    
    top_handsets_df = handset_counts.reset_index()
    top_handsets_df.columns = ['Handset Type', 'Frequency']
    return top_handsets_df

def identify_top_manufacturers(handsets_data):
    
    manufacturer_counts = handsets_data.groupby('Handset Manufacturer')['Handset Type'].count()
   
    top_3_manufacturers = manufacturer_counts.nlargest(3)
    
    top_manufacturers_df = top_3_manufacturers.reset_index()
    top_manufacturers_df.columns = ['Handset Manufacturer', 'Frequency']
    return top_manufacturers_df

def identify_top_handsets_per_manufacturer(handsets_data, top_manufacturers):
    
    top_handsets = handsets_data[handsets_data['Handset Manufacturer'].isin(top_manufacturers['Handset Manufacturer'])]
    
    top_handsets_per_manufacturer = top_handsets.groupby(['Handset Manufacturer', 'Handset Type']).size().unstack(fill_value=0)
    top_handsets_per_manufacturer = top_handsets_per_manufacturer.apply(lambda x: x.nlargest(5), axis=1)
    
    top_handsets_per_manufacturer = top_handsets_per_manufacturer.stack().reset_index()
    top_handsets_per_manufacturer.columns = ['Handset Manufacturer', 'Handset Type', 'Frequency']
    return top_handsets_per_manufacturer


from database import get_connection

def load_cleaned_data():
    """
    Load the cleaned data from PostgreSQL database.
    """
    conn = get_connection()
    query = "SELECT * FROM cleaned_xdr_data;"
    data = pd.read_sql_query(query, conn)
    conn.close()
    return data

def aggregate_user_data(data):
   
    user_aggregation = data.groupby('MSISDN/Number').agg(
        total_sessions=('Bearer Id', 'count'),
        total_duration_ms=('Dur. (ms)', 'sum'),
        total_download_bytes=('Total DL (Bytes)', 'sum'),
        total_upload_bytes=('Total UL (Bytes)', 'sum'),
        social_media_dl_bytes=('Social Media DL (Bytes)', 'sum'),
        google_dl_bytes=('Google DL (Bytes)', 'sum'),
        email_dl_bytes=('Email DL (Bytes)', 'sum'),
        youtube_dl_bytes=('Youtube DL (Bytes)', 'sum'),
        netflix_dl_bytes=('Netflix DL (Bytes)', 'sum'),
        gaming_dl_bytes=('Gaming DL (Bytes)', 'sum'),
        other_dl_bytes=('Other DL (Bytes)', 'sum')
    ).reset_index()

    # Rename columns for clarity
    user_aggregation.columns = [
        'User MSISDN',
        'Total Sessions',
        'Total Duration (ms)',
        'Total Download (Bytes)',
        'Total Upload (Bytes)',
        'Social Media Download (Bytes)',
        'Google Download (Bytes)',
        'Email Download (Bytes)',
        'YouTube Download (Bytes)',
        'Netflix Download (Bytes)',
        'Gaming Download (Bytes)',
        'Other Download (Bytes)'
    ]
    return user_aggregation

def save_to_csv(data, filename='user_engagement_summary.csv'):
    """
    Save the aggregated user data to a CSV file.
    """
    data.to_csv(filename, index=False)


