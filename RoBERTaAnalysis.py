# Sentiment Analysis with RoBERTa
# This Python script performs sentiment analysis on text data using the RoBERTa model. Follow these steps to use the code:

# 1. Dependencies:
#    - Make sure you have the required Python packages installed:
#      - pandas (for data handling)
#      - transformers (for RoBERTa model and tokenizer)
#      - scipy (for softmax function)
#    - You can install them using pip:
#      pip install pandas transformers scipy

# 2. Data Preparation:
#    - Ensure your data is in CSV format.
#    - Verify that the CSV file contains a column with text data.
#    - If your column names are different from 'Tweet Content,' adjust line 71 accordingly.

# 3. Replace File Path:
#    - Set 'target_file' (line 42) to the path of your CSV file. Use double backslashes (\\) for file paths on Windows.

# 4. Run the Code:
#    - Execute this script to perform sentiment analysis on the data.
#    - RoBERTa will calculate sentiment scores for each text entry.
#    - The sentiment scores will be added to a new 'scores' column in the CSV file.

# 5. Output:
#    - The code will save the updated data back to the same CSV file.
#    - The sentiment scores can help you analyze the sentiment of the text data.

# Note: Ensure that you have proper permissions to read and write to the CSV file.
import csv
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax

# Load ROBERTA and tokenizer
roberta = "cardiffnlp/twitter-roberta-base-sentiment"
model = AutoModelForSequenceClassification.from_pretrained(roberta)
tokenizer = AutoTokenizer.from_pretrained(roberta)
labels = ['Negative', 'Neutral', 'Positive']

# Load the CSV file
target_file = "C:\\Users\\jesse\\Desktop\\DDHW\\Testing\\01-Tweet_Data\\20231024_merged_data_Bitcoin.csv"
# Replace with the path to your CSV file
# and change "\" into "\\"!!!!!!
df = pd.read_csv(target_file)

# Define a function to perform sentiment analysis
def perform_sentiment_analysis(tweet):
    tweet_words = []

    for word in tweet.split(' '):
        if word.startswith('@') and len(word) > 1:
            word = '@user'
        elif word.startswith('http'):
            word = "http"
        tweet_words.append(word)

    tweet_proc = " ".join(tweet_words)
    encoded_tweet = tokenizer(tweet_proc, return_tensors='pt')

    output = model(**encoded_tweet)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)

    # Calculate the final sentiment score
    positive_score = scores[2]
    negative_score = scores[0]
    return positive_score - negative_score

# Perform sentiment analysis and add scores to the DataFrame
df['scores'] = df['Tweet Content'].apply(perform_sentiment_analysis)

# Save the DataFrame back to the CSV file
df.to_csv(target_file, index=False)

print("RoBERTa Analysis Complete!")
