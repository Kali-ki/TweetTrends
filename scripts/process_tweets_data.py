import pandas as pd
import ast

def generate_link(hashtag, year):
    link = "https://twitter.com/search?q=(%23" + hashtag + ")%20lang%3Afr%20until%3A" + year + "-12-31%20since%3A" + year + "-01-01&src=typed_query"
    return link

# Read CSV file with pandas
df_tweets = pd.read_csv('../data/tweets.csv')

# Keep only tweets with lang='fr'
df_tweets = df_tweets[df_tweets["lang"] == "fr"]

# Drop the lang column
df_tweets.drop(columns = ["lang"], inplace = True)

# Reset index
df_tweets.reset_index(drop = True, inplace = True)

# List of 12 dataframes, one for each year
list_df_tweets = []

# Fill the list of dataframes with the tweets of each year
for year in range(2010, 2023):
    list_df_tweets.append(df_tweets[df_tweets["created_at"].str.contains(str(year))])

# --- Get the most popular hashtags for year 2010 to 2022 ---

# Set the base year and the number of years to consider
base = 2010
number_of_years = 12

# Create new DataFrame to store the most used hashtags for each year
df_hashtags = pd.DataFrame()

# Loop over the list of dataframes
for i in range(number_of_years+1):

    # Get the hashtags of the tweets of the year
    df_tweets_year_i = list_df_tweets[i]
    df_tweets_year_i_hashtags = df_tweets_year_i["hashtags"]

    # Reset index
    df_tweets_year_i_hashtags.reset_index(drop = True, inplace = True)

    # Convert the hashtags from string to list and store them in a list
    list_hashtags_year_i = []
    for j in range(len(df_tweets_year_i_hashtags)):
        # Upper the hashtags
        l = df_tweets_year_i_hashtags[j].upper()
        # Convert the string to a list
        l = ast.literal_eval(l)
        list_hashtags_year_i += l

    # Convert the list to a pandas series
    series_hashtags_year_i = pd.Series(list_hashtags_year_i)
    
    # Drop the hashtags that are not wanted
    list_not_wanted_hashtags = ["CONCOURS", "RT", "FB", "FF", "LT", "ON", "LRT", "FACEBOOK"]
    for hashtag in list_not_wanted_hashtags:
        series_hashtags_year_i = series_hashtags_year_i[series_hashtags_year_i != hashtag]
    
    # Drop the hashtags which contains word "TOPACHAT"
    series_hashtags_year_i = series_hashtags_year_i[~series_hashtags_year_i.str.contains("TOPACHAT")]

    # Keep only the 10 most popular hashtags
    series_hashtags_year_i = series_hashtags_year_i.value_counts().head(10)

    # Get the 10 most popular hashtags
    print("Most used hashatag in year", str(base+i), ":")
    print(series_hashtags_year_i,"\n")

    # Generate the link for each hashtag and store them in a series
    series_link = pd.Series(series_hashtags_year_i.index).apply(lambda tuple: generate_link(tuple, str(base+i)))
    series_link.name = "context link"

    # Place hashtags as columns and their score as values -> convert the series to a dataframe
    df_hashtags_year_i = series_hashtags_year_i.reset_index()
    # Rename the columns
    df_hashtags_year_i.columns = [base+i, "score "+str(base+i)]

    # Merge the dataframe and the series in df_hashtags
    df_hashtags = pd.concat([df_hashtags, df_hashtags_year_i, series_link], axis = 1)

# Save the dataframe to a csv file
df_hashtags.to_csv("../data/most_used_hashtags.csv", index = False)
