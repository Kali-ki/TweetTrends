#--------------------------------------------------------------------------------------------------
# Description: This script is used to shape the tweets dataset (json)
# into a CSV file with the following columns : created_at, hashtags.
# -------------------------------------------------------------------------------------------------

import os
import pandas as pd

# Function to parse elements of a tweet
def parse(tweet, kw):
    res = dict(tweet)[kw]
    return res

# Function to parse the hashtags
def parse_hashtags(list_hashtags):
    res = []
    for i in range(len(list_hashtags)):
        res.append(list_hashtags[i]["text"])
    return res

# Path to the JSON file
path = os.path.join(os.path.dirname(__file__), '../../data/tweets/tweet_dataset.json')
# Read JSON file with pandas
df_tweets_ = pd.read_json(path)

# Select only the raw_value column
df_tweets_ = df_tweets_["raw_value"]

# Create empty dataframe
df_tweets = pd.DataFrame()

# Create a list of keys to extract
keys = ["created_at", "entities", "lang"]
# Extract the keys and add them to the dataframe
for key in keys :
    df_tweets[key] = df_tweets_.apply(parse, kw = key)

# Extract the hashtags
df_tweets_entities = df_tweets["entities"]
df_tweets_hashtags = pd.DataFrame(df_tweets_entities.apply(parse, kw = "hashtags"))["entities"]
df_tweets["hashtags"] = df_tweets_hashtags.apply(parse_hashtags)

# Drop the entities column
df_tweets.drop(columns = ["entities"], inplace = True)

# Path to the CSV file
path = os.path.join(os.path.dirname(__file__), '../../data/tweets/tweets.csv')
# Save the dataframe as a CSV file
df_tweets.to_csv(path, index = False)