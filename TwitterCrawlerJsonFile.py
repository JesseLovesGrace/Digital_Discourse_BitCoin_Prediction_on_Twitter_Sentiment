import requests
import json
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

# Replace with your Twitter API v2 Bearer Token
bearer_token = config['twitterAPI']['bearer_token']

# Define the Twitter username of the user you want to search tweets from
username = "elonmusk" 

# Define the search query to find tweets about "SpaceX" from the specified user
search_query = f"from:{username} SpaceX"

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

    # Save the data to a JSON file
    json_filename = "tweets.json"
    with open(json_filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    print(f"Collected tweets and saved to {json_filename}")
else:
    print(f"Request returned an error: {response.status_code} {response.text}")
