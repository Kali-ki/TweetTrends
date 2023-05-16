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

# Read JSON file with pandas
df_tweets_ = pd.read_json('../../data/tweet_dataset.json')

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

# Save the dataframe as a CSV file
df_tweets.to_csv('../../data/tweets.csv', index = False)