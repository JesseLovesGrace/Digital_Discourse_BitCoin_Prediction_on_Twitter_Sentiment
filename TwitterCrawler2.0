# This code would be able to handle som exceptions 
# Now it can store the scraped result to  both ".csv" file and ".json" file
# with the files' names in the fromat of "date + twitteruser + keyword" 
# so that yout don't have to rename the file again after the scrape

# Please subscribe to Twitter API V2 Basic level before using this!!!!!!!

import requests
import json
import csv
from datetime import datetime
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

# Replace with your Twitter API v2 Bearer Token
bearer_token = config['twitterAPI']['bearer_token']

# Define the Twitter username of the user you want to search tweets from
username = "brian_armstrong"

# Define the search query keywords
keyword = "Bitcoin"

# Define the search query to find tweets about "SpaceX" from the specified user
search_query = f"from:{username} {keyword}"

# Set the Twitter API v2 endpoint for recent tweet search
url = "https://api.twitter.com/2/tweets/search/recent"

# Define query parameters to include additional fields, including full tweet content
params = {
    "query": search_query,
    "max_results": 100,  # Specify the number of results per response
    "tweet.fields": "created_at,public_metrics,referenced_tweets",  # Include additional fields for full tweet content
    "user.fields": "username",  # Include the username field to retrieve the username
}

# Set the request headers with the Bearer Token
headers = {
    "Authorization": f"Bearer {bearer_token}",
}

# Send a GET request to the endpoint
response = requests.get(url, params=params, headers=headers)
if response.status_code == 200:
    data = response.json()

    if "data" in data:
        # Define a list of tweet data to be written to a CSV file
        tweet_data = []

        for tweet in data["data"]:
            timestamp = datetime.strptime(tweet["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
            username = username
            tweet_content = tweet["text"]
            retweets = tweet["public_metrics"]["retweet_count"]
            likes = tweet["public_metrics"]["like_count"]
            replies = tweet["public_metrics"]["reply_count"]

            # Append the tweet data to the list
            tweet_data.append([timestamp, username, tweet_content, retweets, likes, replies])

        # Define the CSV filename
        date_str = datetime.now().strftime("%Y-%m-%d")
        csv_filename = f"{date_str}_{username}_SpaceX_tweets.csv"

        # Write the tweet data to a CSV file
        with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            # Write the header row
            writer.writerow(["Timestamp", "Username", "Tweet Content", "Retweets", "Likes", "Replies"])
            # Write the tweet data
            writer.writerows(tweet_data)

        print(f"Collected {len(tweet_data)} tweets and saved to {csv_filename}")
    else:
        print("No tweet data found for the given search query.")
else:
    print(f"Request returned an error: {response.status_code} {response.text}")
