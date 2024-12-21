import pandas as pd

def preprocess(df, region_df):
    #take the summer season data
    df = df[df['Season'] == 'Summer']
    #merge the data with region_df
    df = df.merge(region_df, on='NOC', how='left')
    #drop the duplicate values
    df.drop_duplicates(inplace=True)
    #one hot encoding for the medal column
    df = pd.concat([df, pd.get_dummies(df['Medal'], dtype=int)], axis=1)
    return df
