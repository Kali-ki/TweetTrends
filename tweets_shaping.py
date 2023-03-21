import numpy as np
import pandas as pd

# Read JSON file with pandas
tweets = pd.read_json('tweet_dataset.json', lines=True, encoding='utf-8')

# Show head of tweets
print(tweets.head())