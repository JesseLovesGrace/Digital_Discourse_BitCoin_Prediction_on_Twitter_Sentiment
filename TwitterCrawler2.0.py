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
username = "BTC_Archive"

# Define the search query keywords
keywords = "Bitcoin"

# Define the search query to find tweets about the specified keywords from the specified user
search_query = f"from:{username} {keywords}"

# Set the Twitter API v2 endpoint for recent tweet search
url = "https://api.twitter.com/2/tweets/search/recent"

# Define query parameters to include additional fields
params = {
    "query": search_query,
    "max_results": 100,  # Specify the number of results per response
    "tweet.fields": "created_at,text,public_metrics,referenced_tweets",  # Include additional fields
}

# Set the request headers with the Bearer Token
headers = {
    "Authorization": f"Bearer {bearer_token}",
}

# Send a GET request to the endpoint
response = requests.get(url, params=params, headers=headers)

if response.status_code == 200:
    data = response.json()

    # Define a list of tweet data to be written to a CSV file
    tweet_data_csv = []

    # Define a list of tweet data to be written to a JSON file
    tweet_data_json = []

    for tweet in data["data"]:
        timestamp = datetime.strptime(tweet["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
        username = username
        tweet_content = tweet["text"]
        retweets = tweet["public_metrics"]["retweet_count"]
        likes = tweet["public_metrics"]["like_count"]
        replies = tweet["public_metrics"]["reply_count"]

        # Append the tweet data to the CSV and JSON lists
        tweet_data_csv.append([timestamp, username, tweet_content, retweets, likes, replies])
        tweet_data_json.append({
            "Timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "Username": username,
            "Tweet Content": tweet_content,
            "Retweets": retweets,
            "Likes": likes,
            "Replies": replies,
        })

    # Get the current date
    current_date = datetime.now().strftime("%Y%m%d")

    # Define the CSV filename with date, username, and keywords
    csv_filename = f"{current_date}_{username}_{keywords}.csv"
    # Define the JSON filename with date, username, and keywords
    json_filename = f"{current_date}_{username}_{keywords}.json"

    # Write the tweet data to a CSV file
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        # Write the header row
        writer.writerow(["Timestamp", "Username", "Tweet Content", "Retweets", "Likes", "Replies"])
        # Write the tweet data
        writer.writerows(tweet_data_csv)

    # Write the tweet data to a JSON file
    with open(json_filename, 'w', encoding='utf-8') as json_file:
        json.dump(tweet_data_json, json_file, ensure_ascii=False, indent=4)

    print(f"Collected {len(tweet_data_csv)} tweets and saved to {csv_filename} and {json_filename}")
else:
    print(f"Request returned an error: {response.status_code} {response.text}")

