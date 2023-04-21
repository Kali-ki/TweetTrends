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

for i in range(number_of_years+1):

    df_tweets_year_i = list_df_tweets[i]
    df_tweets_year_i_hashtags = df_tweets_year_i["hashtags"]
    df_tweets_year_i_hashtags.reset_index(drop = True, inplace = True)

    list_hashtags_year_i = []

    for j in range(len(df_tweets_year_i_hashtags)):
        l = ast.literal_eval(df_tweets_year_i_hashtags[j])
        list_hashtags_year_i += l

    # Count the number of occurences of each hashtag
    series_hashtags_year_i = pd.Series(list_hashtags_year_i)

    # Get the 10 most popular hashtags
    print("Most used hashatag in year",str(base+i),":")
    print(series_hashtags_year_i.value_counts().head(10),"\n")
    