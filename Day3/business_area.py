def eda_business_area(df):
    for col in ['business_area','business_subarea']:
        df[col] = df[col].str.lower()
        df[col] = df[col].str.replace(" ", "") 
        df[col] = df[col].str.replace(r'[^\w\s]', "") 
        df[col] = df[col].fillna('nan') 
    df['total_area'] = df['business_area'].astype(str) + df['business_subarea'].astype(str)
    return df 