import pandas as pd
import ast

# Read CSV file with pandas
df_tweets = pd.read_csv('../data/tweets.csv')

# Keep only tweets with lang='fr'
df_tweets = df_tweets[df_tweets["lang"] == "fr"]

# Reset index
df_tweets.reset_index(drop = True, inplace = True)

# Drop the lang column
df_tweets.drop(columns = ["lang"], inplace = True)

# List of 12 dataframes, one for each year
list_df_tweets = []

# Fill the list of dataframes with the tweets of each year
for year in range(2010, 2023):
    list_df_tweets.append(df_tweets[df_tweets["created_at"].str.contains(str(year))])

# --- Get the most popular hashtags for year 2010 to 2022 ---

base = 2010
number_of_years = 12

# Loop over the list of dataframes
for i in range(number_of_years+1):

    # Get the hashtags of the tweets of the year
    df_tweets_year_i = list_df_tweets[i]
    df_tweets_year_i_hashtags = df_tweets_year_i["hashtags"]

    # Reset index
    df_tweets_year_i_hashtags.reset_index(drop = True, inplace = True)

    # Convert the hashtags from string to list
    list_hashtags_year_i = []
    for j in range(len(df_tweets_year_i_hashtags)):
        # Upper the hashtags
        l = df_tweets_year_i_hashtags[j].upper()
        l = ast.literal_eval(l)
        list_hashtags_year_i += l

    # Convert the list to a pandas series
    series_hashtags_year_i = pd.Series(list_hashtags_year_i)
    
    # Drop the hashtags that are not wanted
    list_not_wanted_hashtags = ["CONCOURS", "RT", "FB", "FF", "LT", "ON", "LRT", "FACEBOOK"]
    for hashtag in list_not_wanted_hashtags:
        series_hashtags_year_i = series_hashtags_year_i[series_hashtags_year_i != hashtag]

    # Get the 15 most popular hashtags
    print("Most used hashatag in year", str(base+i), ":")
    print(series_hashtags_year_i.value_counts().head(15),"\n")
    