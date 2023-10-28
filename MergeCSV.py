# CSV File Merger and Sorter
# This Python script allows you to merge and sort multiple CSV files containing tweet data.
# Follow these steps to use the code:

# 1. Set Directory:
#    - Specify the directory where your CSV files are located by setting the 'directory' variable.
#    - Ensure you provide the correct path to the directory containing your CSV files.

# 2. Run the Code:
#    - Execute this script to merge and sort the CSV files.
#    - The code will extract and merge data from multiple CSV files, sort it by 'Username' and 'Timestamp',
#      and save the sorted data to a new CSV file.
#    - The new CSV file will be named with the current date and labeled as '_merged_data.csv'.
#    - The sorted data is saved in the 'Testing' directory. You can customize this path if needed.

# Customize the code by modifying variables to meet your specific needs. Enjoy merging and sorting your CSV files!

# Note: Make sure to provide the correct directory path and have proper permissions to read and write files.

import os
import glob
import pandas as pd
from datetime import datetime

# Set the directory where your CSV files are located
directory = "C:\\Users\\jesse\\Desktop\\DDHW\\CSV"  # Replace with your directory path

# List all CSV files in the directory
csv_files = glob.glob(os.path.join(directory, "*.csv"))

# Create an empty list to store DataFrames
dataframes = []

# Iterate through CSV files and handle exceptions
for file in csv_files:
    try:
        df = pd.read_csv(file)
        # Extract only the date part from the 'Timestamp' column
        df['Timestamp'] = pd.to_datetime(df['Timestamp']).dt.date
        dataframes.append(df)
    except Exception as e:
        print(f"Error while reading {file}: {str(e)}")

# Check if any CSV files were successfully read
if not dataframes:
    print("No valid CSV files found in the specified directory.")
else:
    # Concatenate all DataFrames into one
    merged_df = pd.concat(dataframes, ignore_index=True)

    # Sort the merged DataFrame by 'Username' and 'Timestamp'
    sorted_df = merged_df.sort_values(by=['Username', 'Timestamp'])

    # Generate the output filename with the current date
    current_date = datetime.now().strftime("%Y%m%d")
    output_csv = f"C:\\Users\\jesse\\Desktop\\DDHW\\Testing\\{current_date}_merged_data.csv"

    # Save the sorted DataFrame to the new CSV file
    sorted_df.to_csv(output_csv, index=False)

    print(f'Merged and sorted data saved to {output_csv}')
