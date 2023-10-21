import pandas as pd

# Directories, variables, and parameters:

# Tweet Raw File Directory
tweet_raw_file_dir = "C:\\Users\\jesse\\Desktop\\DDHW\\Testing\\20231017_merged_data.csv"
# Bitcoin Price Raw File Directory
bitcoin_price_file_dir = "C:\\Users\\jesse\\Desktop\\DDHW\\Testing\\HKEX-03066.csv"
# Target Directory for Storing New Files
target_directory = "C:\\Users\\jesse\\Desktop\\DDHW\\Testing\\"

# Step 1: Sort Data by Timestamp
df = pd.read_csv(tweet_raw_file_dir)
df['Timestamp'] = pd.to_datetime(df['Timestamp'])
df = df.sort_values(by='Timestamp', ascending=False)

# Step 2: Calculate Sentiment Index
df['Sentiment_Index'] = df['Likes'] * df['scores']

# Step 3: Group Data by Date and Sum Sentiment_Index
df['Date'] = df['Timestamp'].dt.date
processed_data = df.groupby('Date')['Sentiment_Index'].sum().reset_index()

# Step 4: Create and Save Processed Data with a Specified Filename
output_file_path = target_directory + 'processed_sentiment_index_by_date.csv'
processed_data.to_csv(output_file_path, index=False)

# Step 5: Merge Sentiment_Index with Price_Next_Day

# Read data from both files
sentiment_df = pd.read_csv(output_file_path)
bitcoin_df = pd.read_csv(bitcoin_price_file_dir)

# Convert date columns to datetime format
sentiment_df['Date'] = pd.to_datetime(sentiment_df['Date'])
bitcoin_df['Date'] = pd.to_datetime(bitcoin_df['Date'])

# Shift the Bitcoin price values by one day to create the "price_next_day" column
bitcoin_df['Nominal Price'] = bitcoin_df['Nominal Price'].shift(+1)

# Merge data based on the date column
merged_df = sentiment_df.merge(bitcoin_df, on='Date', how='left')

# Overwrite the existing file with the merged data
merged_df.to_csv(output_file_path, index=False)
