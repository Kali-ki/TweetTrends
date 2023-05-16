#--------------------------------------------------------------------------------------------------
# Description: This script is used to scrap tweets from TopHashtags user.
# Scraping is done by day, from 2010-01-01 to 2022-01-01.
# --------------------------------------------------------------------------------------------------

import stweet as st
import arrow

# Search tweets from a user, between two dates, and only original tweets (no responses).
def try_search(username, date_start, date_end, filter=st.RepliesFilter.ONLY_ORIGINAL):
    search_tweets_task = st.SearchTweetsTask(from_username=username, since=date_start, until=date_end, replies_filter=filter)
    output_jl_tweets = st.JsonLineFileRawOutput('output_raw_search_tweets.jl')
    output_jl_users = st.JsonLineFileRawOutput('output_raw_search_users.jl')
    output_print = st.PrintRawOutput()
    st.TweetSearchRunner(search_tweets_task=search_tweets_task,
                         tweet_raw_data_outputs=[output_print, output_jl_tweets],
                         user_raw_data_outputs=[output_print, output_jl_users]).run()

# Loop on year, month, day since 2010-01-01 to 2022-01-01
d1 = arrow.Arrow(2010, 1, 1)
d2 = arrow.Arrow(2023, 1, 1)
while d1 < d2:
    try_search("TopHashtags", date_start=d1, date_end=d1.shift(days=+1))
    d1 = d1.shift(days=+1)