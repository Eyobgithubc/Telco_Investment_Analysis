def identify_top_handsets(handsets_data):
    handset_counts = handsets_data['handset'].value_counts().head(10)
    return handset_counts

def identify_top_manufacturers(handsets_data):
    manufacturer_counts = handsets_data.groupby('manufacturer')['handset'].count()
    top_3_manufacturers = manufacturer_counts.nlargest(3)
    return top_3_manufacturers

def identify_top_handsets_per_manufacturer(handsets_data, top_manufacturers):
    top_handsets = handsets_data[handsets_data['manufacturer'].isin(top_manufacturers.index)]
    top_handsets_per_manufacturer = top_handsets.groupby('manufacturer')['handset'].value_counts().groupby(level=0).head(5)
    return top_handsets_per_manufacturer
