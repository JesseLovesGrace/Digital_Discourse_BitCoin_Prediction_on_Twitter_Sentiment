# Twitter Tweet Scraper
# This Python script allows you to scrape and store tweets from a specific Twitter user that contain certain keywords.
# The screped information would be stored under the same directory of your Python file
# Follow these steps to use the code:

# 1. Prerequisites:
#    - Make sure you have obtained a Twitter API v2 Bearer Token. You can subscribe to Twitter API V2 Basic level.
#    - Store your Bearer Token in the 'config.ini' file. Replace 'your_bearer_token' with your actual token.

# 2. Customize Your Search:
#    - Specify the Twitter username of the user you want to scrape tweets from by setting the 'username' variable.
#    - Define the search query keywords by setting the 'keyword' variable. This will find tweets that match both the username and the keyword.

# 3. Run the Code:
#    - Execute this script to scrape tweets based on your search criteria.
#    - The code will save the collected tweets to both a CSV and a JSON file with filenames in the format 'date_username_keyword'.
#    - Be sure to have proper permissions to read and write files in the script's directory.


# Example of how to execute the code:

# Customize the code by modifying variables to meet your specific needs. Enjoy scraping and analyzing Twitter data!

# Note: Please be mindful of Twitter's API usage policies.


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
username = "krakenfx"

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
        # Define a list of tweet data to be written to CSV and JSON
        tweet_data = []

        for tweet in data["data"]:
            timestamp = datetime.strptime(tweet["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
            username = username
            tweet_content = tweet["text"]
            retweets = tweet["public_metrics"]["retweet_count"]
            likes = tweet["public_metrics"]["like_count"]
            replies = tweet["public_metrics"]["reply_count"]

            # Convert the datetime object to a string
            timestamp_str = timestamp.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

            # Append the tweet data to the list
            tweet_data.append({
                "Timestamp": timestamp_str,
                "Username": username,
                "Tweet Content": tweet_content,
                "Retweets": retweets,
                "Likes": likes,
                "Replies": replies
            })

        # Define the CSV filename
        date_str = datetime.now().strftime("%Y-%m-%d")
        csv_filename = f"{date_str}_{username}_{keyword}.csv"

        # Write the tweet data to a CSV file
        with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            # Write the header row
            writer.writerow(["Timestamp", "Username", "Tweet Content", "Retweets", "Likes", "Replies"])
            # Write the tweet data
            for tweet in tweet_data:
                writer.writerow([tweet["Timestamp"], tweet["Username"], tweet["Tweet Content"],
                                 tweet["Retweets"], tweet["Likes"], tweet["Replies"]])

        print(f"Collected {len(tweet_data)} tweets and saved to {csv_filename}")

        # Define the JSON filename
        json_filename = f"{date_str}_{username}_{keyword}.json"

        # Write the tweet data to a JSON file
        with open(json_filename, 'w', encoding='utf-8') as json_file:
            json.dump(tweet_data, json_file, ensure_ascii=False, indent=4)

        print(f"Saved the tweets to {json_filename}")
    else:
        print("No tweet data found for the given search query.")
else:
    print(f"Request returned an error: {response.status_code} {response.text}")
