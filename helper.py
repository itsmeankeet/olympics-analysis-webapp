import numpy as np
import pandas as pd

def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
    medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    return medal_tally


def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')
    countries = np.unique(df['region'].dropna().values).tolist()
    countries.sort()
    countries.insert(0, 'Overall')
    return years, countries

def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if(year == 'Overall' and country == 'Overall'):
        temp_df = medal_df
    if(year == 'Overall' and country != 'Overall'):
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if(year != 'Overall' and country == 'Overall'):
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if(year != 'Overall' and country != 'Overall'):
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]
    if(flag == 1): 
        temp_df = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year', ascending=True).reset_index()
    else:
        temp_df = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
    temp_df['total'] = temp_df['Gold'] + temp_df['Silver'] + temp_df['Bronze']
    return temp_df

def data_over_time(df, col):
    nations_over_time = df.drop_duplicates(['Year',col])['Year'].value_counts().reset_index().sort_values('Year')
    nations_over_time.rename(columns={'Year':'Edition', col:'count'}, inplace=True)
    return nations_over_time

def most_successful(df, sport):
    """Returns DataFrame of most successful athletes by medal count for a given sport"""
    # Filter for valid medals and sport
    temp_df = df[df['Medal'].notna()]
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]
    
    # Group and count medals
    medals = temp_df.groupby(['Name', 'region', 'Sport'])['Medal'].count().reset_index()
    medals = medals.sort_values('Medal', ascending=False)
    medals.columns = ['Name', 'Region', 'Sport', 'Medals']
    # Add index column starting from 0
    medals = medals.reset_index(drop=True)
    # Return top 10 athletes
    return medals.head(15)


def yearwise_medal_tally(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset = ['Team', 'NOC','Games', 'Year','City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df

def country_event_heatmap(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset = ['Team', 'NOC','Games', 'Year','City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    pt = new_df.pivot_table(index= 'Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt


def most_successful_athetics_country(df, country):
    """Returns DataFrame of most successful athletes by medal count for a given sport"""
    # Handle empty dataframe case
    new_df = df.dropna(subset=['Medal'])
    new_df = new_df[new_df['region'] == country]
    
    if len(new_df) == 0:
        # Return empty DataFrame with correct columns if no data
        return pd.DataFrame(columns=['Name', 'Sport', 'Medals'])
        
    medals = new_df.groupby(['Name','Sport']).count()['Medal'].reset_index().sort_values('Medal', ascending=False).head(10)
    medals.columns = ['Name', 'Sport', 'Medals'] 
    medals = medals.reset_index(drop=True)
    return medals

def weight_height(df, sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)
    final.fillna(0, inplace=True)
    return final