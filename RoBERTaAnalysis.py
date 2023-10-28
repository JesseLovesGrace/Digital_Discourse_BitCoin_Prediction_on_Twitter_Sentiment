# If you want to use this code, please install transformer, pandas, numpy and csv
# You can either install them locally or globally and then let your project inherit from global site-package
# but locally is always preferable

# For this code, before doing analysis, please convert your date files into CSV
# Also, be careful with column names because this is what the code reads.
# Modify the column names at line 53, 
# or change your column name into 'Tweet Content' on your CSV file

# All you need is the directory of the file that contains the data,
# Input them on line 24
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
