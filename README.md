# TweetTrends

TweetTrends is a data engineering project to :

- 🔎 Plot dynamically graphs on the evolution of most used hashtags in date range or for a specific hashtags :

![image](https://github.com/Kali-ki/TweetTrends/assets/62034725/5833ff13-b49e-427d-9863-6fc9d8207184)

- 📷 Visualize with images the most used hashtags on Twitter from 2010 to 2022 (with or without background)

![image](https://github.com/Kali-ki/TweetTrends/assets/62034725/400d42d2-71bc-4279-b793-24c78c29a637)


## Description

This project is a data engineering project. The goal is to create an application that uses most used hashtags on Twitter from 2010 to 2022 and do visualizations on them, in the manner of [this page](https://www.visualcapitalist.com/20-years-of-top-trending-google-searches/), that was about top google searches. This way, we can see the evolution of subject on Twitter over the years. This is interesting because,  it often well represents the news of the year. However, it is not a perfect representation of them because many companies use Twitter to promote their products, and people who are talking about their life, without any link to the news.

## Requirements
- `Python >= 3.9`
- `pip`

Install all the required libraries with :
```bash
pip install -r requirements.txt
```
We advice you to have a chromium browser. [Eel](https://github.com/python-eel/Eel) (the library used as UI) works better in this configuration.

## Use the application

The main entrypoint of the application is **app.py**.

```bash
python app.py
```

## Development

> To get more details about the scripts, you can go to the [scripts](scripts/tweets/) folder. All the scripts are documented.

### 📕 Data source

The first step was to find a source for Twitter data. For that, we use all the tweets of the Twitter user [TopHashtags](https://twitter.com/TopHashtags). This user has tweeted the most used hashtags approximately about every day since 2010.

There are a few drawbacks to this method of using tweets of `TopHashtags` :

- **The year 2014 is almost empty**
- We don't have the number of occurences of each hashtags

Despite these drawbacks, we decided to use this method because it was the easiest way to get the data.

### ⚓ Data collecting

For collecting, there was severals solutions :

- Use the Twitter API -> But it is to limited with free account
- Use [Twint](https://github.com/twintproject/twint) -> But we never managed to make it works

Finaly, we used a project inspired by Twint called [Stweet](https://github.com/markowanga/stweet). This library is not as complete as Twint but it was enough for our needs. We used it to get all the tweets of the user [TopHashtags](https://twitter.com/TopHashtags) and save them in a JSON file. This step took about 4 hours to get all the tweets.

### 🚿 Data cleaning

At this step, we had a big JSON file with all the tweets and a plenty of useless informations. So, we needed to clean all of this with a Python script : [tweets_shapping](scripts/tweets/tweets_shaping.py)
On this script, thank's to Pandas, we removed all the useless informations and we kept only the hashtags and the date of the tweet. Then, we saved the result in a CSV file : [tweets.csv](data/tweets/tweets.csv).

Output :

![CSV](assets/csv_1.png)

### 🎯 Data processing

Now, we had a CSV file with all the hashtags and the date of the tweet. But, we needed to count the number of occurences of each hashtags for each year. As before, we used a Python script : [process_tweets_data](scripts/tweets/process_tweets_data.py)

This script is a bit more complex than the previous one. In input, we have the csv file [tweets.csv](data/tweets/tweets.csv), and in output, we have another CSV file but this one only has the hashtags, the numbers of occurences per year and a link to an advanced Twitter search with the hashtag and the year. This way, we can see tweets to get more informations about the hashtag.

Output :

![CSV](assets/csv_2.png)

### 💎 Data visualization

The next step is to visualize the data. To do that, we used a Python script : [plots_tweets.py](scripts/tweets/plots_tweets.py). On this script, we can specify :

- The number of most popular hashtags
- Hashtags we want search
- Hashtags we want to ignore
- The date range we want to search
- The date range to visualize
- If we want to get only french hashtags (hashtags with french context)

*The granularity of the date range is the year, but with somes modifications, it can be changed to month or even to day.*

In output, thanks to Matplotlib and Pandas, we get a graph with the evolution of the hashtags over the years :

![Graph](assets/plot_example.png)

### 🖼️ Image parsing
One the goal of the project was to automatically illustrate keywords. For that, we created 'ImageParser' objects, that aim to find links that illustrate a keyword (find more about it in the scripts/imagelib.py to see the abstract class that defines a parser). 
At first, we tried to use the [Wikipedia API](https://pypi.org/project/Wikipedia-API/), but we add many cases where no image was found (see more in scripts/wikiparser.py).
Then we created the [GImageSerpApiParser](scripts/gimageserpapiparser.py), that finds images with Google Images. It is very efficient, but has a restricted number of api requests, and you need a token. See more about it on [serpapi.com](https://serpapi.com/).  


## Structure of the project

```text
📦 TweetTrends
┣ 📂data
┃ ┣ 📂 tweets
┃ ┃ ┣ 📜 tweets.csv
┃ ┃ ┗ 📜 most_used_hashtags.csv
┃ ┃ ┗ 📜 tweet_dataset.json
┃ ┃ ┗ 📜 tweets_dataset.json
┣ 📂 scripts
┃ ┣ 📂 tweets
┃ ┃ ┣ 📜 process_tweets_data.py
┃ ┃ ┗ 📜 tweets_shaping.py
┃ ┃ ┗ 📜 plots_tweets.py
┃ ┃ ┗ 📜 scrap_tweets.py
┃ ┣ 📜 app.py
┃ ┣ 📜 ui.py
┃ ┣ 📜 uibuilder.py
┃ ┣ 📜 imagelib.py
┗ 📜 .gitignore
┗ 📜 README.md
┗ 📜 requirements.md
```

## Limitations and Improvements

### 🚫 Limitations

The project has one big limitations : the data source. Indeed, we used the tweets of the Twitter user [TopHashtags](https://twitter.com/TopHashtags). And as said previously, there are a few drawbacks and limitations to this method.

Except this, the project has not been really limited by anything else.

### 🚧 Improvements

According to the previous part, the main improvement would be to use another source of data. The Twitter API is probably the best solution if it is possible to pay for it. Otherwise, we can try to find another Twitter user that tweets the most used hashtags every day, or an already existing dataset.

Another possible improvement would be to merge the two scripts [process_tweets_data.py](scripts/tweets/process_tweets_data.py) and [plots_tweets.py](scripts/tweets/plots_tweets.py) to have only one script that does everything. This way, the image representation and the plot would present the same data.

Also, the granularity of the data could be improved. Indeed, we only have the number of occurences of each hashtags per year. But, we could have the number of occurences per month or per day. This way, we could have a more precise representation of the evolution of the hashtags.

And to finnish with the improvements, the UI could be a bit improved. For example, we could add a button to download the CSV file with the data of the plot or add more descriptions of each inputs.
