# -------------------------------------------------------------------------------------------------
# Description: This script plots the evolution of the hashtags through the years.
# Can also search hashtags and plot their evolution.
# -------------------------------------------------------------------------------------------------

import os
import pandas as pd
import matplotlib.pyplot as plt
import ast

# --- Parameters ----------------------------------------------------------------------------------

# NUMBER_TWEETS_TO_KEEP most popular hashtags
NUMBER_TWEETS_TO_KEEP = 10 # Keep at 0 to disable
# Search for the NUMBER_TWEETS_TO_KEEP hashtags
SEARCHED_HASHTAGS = [] # Keep empty to disable

FR_ONLY = True

# Date range for top NUMBER_TWEETS_TO_KEEP tweets
DATE_START_T = 2010 # >= 2010
DATE_END_T = 2022 # <= 2022

# Date range for visualization
DATE_START_V = 2010 # >= 2010
DATE_END_V = 2022 # <= 2022

# Hashtags to drop
HASHTAGS_TO_DROP = ["CONCOURS", "RT", "FB", "FF", "LT", "ON", "LRT", "FACEBOOK"]

def plot(NUMBER_TWEETS_TO_KEEP=NUMBER_TWEETS_TO_KEEP, 
         SEARCHED_HASHTAGS=SEARCHED_HASHTAGS, 
         FR_ONLY=FR_ONLY,
         DATE_START_T=DATE_START_T,
         DATE_END_T=DATE_END_T, 
         DATE_START_V=DATE_START_V,
         DATE_END_V=DATE_END_V,
         HASHTAGS_TO_DROP=HASHTAGS_TO_DROP):

    # --- Parameters Check ----------------------------------------------------------------------------

    if(NUMBER_TWEETS_TO_KEEP < 0):
        print("Error: NUMBER_TWEETS_TO_KEEP < 0")
        exit()

    if(NUMBER_TWEETS_TO_KEEP == 0 and SEARCHED_HASHTAGS == []):
        print("Error: NUMBER_TWEETS_TO_KEEP == 0 and SEARCHED_HASHTAGS != []")
        exit()

    if(DATE_START_T > DATE_END_T):
        print("Error: DATE_START_V < DATE_START_T")
        exit()

    if(DATE_START_V > DATE_END_V):
        print("Error: DATE_END_V > DATE_END_T")
        exit()

    if(DATE_START_T < 2010):
        print("Error: DATE_START_T < 2010")
        exit()

    if(DATE_END_T > 2022):
        print("Error: DATE_END_T > 2022")
        exit()

    if(DATE_START_V < 2010):
        print("Error: DATE_START_V < 2010")
        exit()

    if(DATE_END_V > 2022):
        print("Error: DATE_END_V > 2022")
        exit()

    # --- Function -----------------------------------------------------------------------------------

    # Convert the hashtags to a Series
    def convert_hashtags_to_list(df_tweets_hashtags):
        list_hashtags_year_i = []
        for j in range(len(df_tweets_hashtags)):
            # Upper the hashtags
            l = df_tweets_hashtags[j].upper()
            # Convert the string to a list
            l = ast.literal_eval(l)
            list_hashtags_year_i += l
        
        return pd.Series(list_hashtags_year_i)

    # --- Main ----------------------------------------------------------------------------------------

    # Path to the CSV file
    path = os.path.join(os.path.dirname(__file__), '../../data/tweets/tweets.csv')

    # Read CSV file with pandas
    df_tweets = pd.read_csv(path)

    if(FR_ONLY):
        # Keep only tweets with lang='fr'
        df_tweets = df_tweets[df_tweets["lang"] == "fr"]
        # Drop the lang column
        df_tweets.drop(columns = ["lang"], inplace = True)

    # Reset index
    df_tweets.reset_index(drop = True, inplace = True)

    # --- Get hashtags for year DATE_START_T to DATE_END_T ------------------------------------

    list_hashtags = []

    if(NUMBER_TWEETS_TO_KEEP != 0):

        # Keep only tweets between DATE_START_T and DATE_END_T
        df_tweets_dated = pd.DataFrame()
        for year in range(DATE_START_T, DATE_END_T+1):
            tmp = df_tweets[df_tweets["created_at"].str.contains(str(year))]
            df_tweets_dated = pd.concat([df_tweets_dated, tmp])

        # Get the hashtags of the tweets
        df_tweets_hashtags = df_tweets_dated["hashtags"]

        # Reset index
        df_tweets_hashtags.reset_index(drop = True, inplace = True)

        series_hashtags = convert_hashtags_to_list(df_tweets_hashtags)

        for hashtag in HASHTAGS_TO_DROP:
            series_hashtags = series_hashtags[series_hashtags != hashtag]

        list_hashtags = series_hashtags.value_counts().head(NUMBER_TWEETS_TO_KEEP).index.tolist()

    list_hashtags = list_hashtags + SEARCHED_HASHTAGS

    # --- Get evolution of the most popular hashtags for year 2010 to 2022 ----------------------------

    df = pd.DataFrame()

    for year in range(DATE_START_V, DATE_END_V+1):
        df_tweet_year = df_tweets[df_tweets["created_at"].str.contains(str(year))]

        # Get the hashtags of the tweets and reset index
        df_tweets_year_i_hashtags = df_tweet_year["hashtags"]
        df_tweets_year_i_hashtags.reset_index(drop = True, inplace = True)

        # Convert the list to a pandas series
        series_hashtags_year_i = convert_hashtags_to_list(df_tweets_year_i_hashtags)

        # Count the number of occurences of each hashtag
        series_hashtags_year_i = series_hashtags_year_i.value_counts()

        # Keep only the 10 most popular hashtags all years
        series_hashtags_year_i = series_hashtags_year_i[series_hashtags_year_i.index.isin(list_hashtags)]
        
        # Rename the series
        series_hashtags_year_i.name = year
        # Concatenate the series to the dataframe
        df = pd.concat([df, series_hashtags_year_i], axis = 1)

    df = df.fillna(0)
    df = df.transpose()

    # --- Plot ----------------------------------------------------------------------------------------

    if(df.empty):
        print("No tweets found")
        exit()

    # Plot the evolution of the most popular hashtags through the years
    df.plot()
    plt.legend(loc = "upper right")
    plt.title("Evolution of the most popular hashtags through the years")
    plt.xlabel("Year")
    plt.ylabel("Number of occurences")

    return plt