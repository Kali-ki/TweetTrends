import numpy as np
import pandas as pd

# Read JSON file with pandas
tweets = pd.read_json('tweet_dataset.json', lines=True)

# Get only "rawdata" part
tweets = tweets['raw_value']

# Cast in dictionary
tweets = tweets.to_dict()

# Get only the text of the tweets
print(tweets[0])