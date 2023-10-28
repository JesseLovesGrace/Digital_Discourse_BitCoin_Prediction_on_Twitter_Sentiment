# Twitter Tweet Collector
# This Python script allows you to collect tweets related to a specific keyword using Twitter API v2.
# Follow these steps to use the code:

# 1. Set Up Your Environment:
#    - Before running this code, ensure you have installed necessary dependencies such as "requests,"
#      and "configparser." You can install these packages using pip:
#      pip install requests configparser

# 2. Customize Configuration:
#    - Edit the 'config.ini' file to add your Twitter API v2 Bearer Token.
#    - Replace 'config.ini' with the actual path if it's in a different directory.

# 3. Define Your Search:
#    - Set your desired keyword by updating the 'key_word' variable.
#    - Adjust the maximum number of tweets you want to collect by modifying the 'max_tweets' variable.

# 4. Specify Output Directories:
#    - Define the directory paths where the CSV and JSON files will be saved by updating 'csv_directory' and 'json_directory'.
#    - Make sure to use double backslashes "\\" in the directory path for proper formatting.

# 5. Run the Code:
#    - Execute this script to collect tweets based on your search query.
#    - The collected tweets will be saved in both CSV and JSON files with filenames containing the current date and your keyword.

# Customize the code by modifying variables to meet your specific needs. Enjoy collecting and analyzing Twitter data!

# Note: Make sure you have access to the Twitter API and a valid Bearer Token.

import os
import requests
import json
import csv
from datetime import datetime
import configparser

# Define the search query keyword (e.g., "Tesla")
key_word = "Tesla"  # Update the keyword here
# Replace with your desired directory path for CSV files
csv_directory = "C:\\Users\\jesse\\Desktop\\DDHW2\\CSV"
# Replace with your desired directory path for JSON files
json_directory = "C:\\Users\\jesse\\Desktop\\DDHW2\\JSON"

# Define the maximum number of tweets you want to collect (e.g., 350)
max_tweets = 350

def save_files(tweet_data, csv_directory, json_directory):
    # Define the CSV filename
    date_str = datetime.now().strftime("%Y-%m-%d")
    csv_filename = os.path.join(csv_directory, f"{date_str}_{key_word}.csv")

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
    json_filename = os.path.join(json_directory, f"{date_str}_{key_word}.json")

    # Write the tweet data to a JSON file
    with open(json_filename, 'w', encoding='utf-8') as json_file:
        json.dump(tweet_data, json_file, ensure_ascii=False, indent=4)

    print(f"Saved the tweets to {json_filename}")

config = configparser.ConfigParser()
config.read('config.ini')

# Replace with your Twitter API v2 Bearer Token
bearer_token = config['twitterAPI']['bearer_token']

# Define the search query to find tweets related to the "key_word" with likes over 10,000 and retweets over 10,000
search_query = f"{key_word}"

# Set the Twitter API v2 endpoint for recent tweet search
url = "https://api.twitter.com/2/tweets/search/recent"

# Define query parameters to include additional fields, including full tweet content
params = {
    "query": search_query,
    "max_results": 10,  # Specify the number of results per response
    "tweet.fields": "created_at,public_metrics,referenced_tweets",
    # Include additional fields for full tweet content
    "user.fields": "username",  # Include the username field to retrieve the username
}

# Set the request headers with the Bearer Token
headers = {
    "Authorization": f"Bearer {bearer_token}",
}

# Send GET requests until you reach the maximum number of tweets
total_tweets = 0
tweet_data = []

while total_tweets < max_tweets:
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}")
        response = None  # Set the response to None to handle it later

    if response and response.status_code == 200:
        data = response.json()

        if "data" in data:
            for tweet in data["data"]:
                timestamp = datetime.strptime(tweet["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ")

                # To handle cases where the user ID is nested within referenced_tweets
                user_info = tweet.get("referenced_tweets", [{}])[0].get("type") == "retweeted" and \
                            tweet.get("referenced_tweets", [{}])[0].get("id")

                if user_info:
                    username = user_info
                else:
                    username = tweet.get("author_id")

                tweet_content = tweet["text"]
                retweets = tweet["public_metrics"]["retweet_count"]
                likes = tweet["public_metrics"]["like_count"]
                replies = tweet["public_metrics"]["reply_count"]

                # Convert the datetime object to a string in the format "YYYY-MM-DD"
                timestamp_str = timestamp.strftime("%Y-%m-%d")

                # Append the tweet data to the list
                tweet_data.append({
                    "Timestamp": timestamp_str,
                    "Username": username,
                    "Tweet Content": tweet_content,
                    "Retweets": retweets,
                    "Likes": likes,
                    "Replies": replies
                })

                total_tweets += 1

            # If we reached the maximum number of tweets, break the loop
            if total_tweets >= max_tweets:
                break
        else:
            print("No tweet data found for the given search query.")
            break
    else:
        if response:
            print(f"Request returned an error: {response.status_code} {response.text}")
        else:
            print("No response received.")
        break

# Define the directory to save CSV and JSON files
csv_dir = csv_directory
json_dir = json_directory

# Call the save_files function to save the CSV and JSON files
save_files(tweet_data, csv_dir, json_dir)
