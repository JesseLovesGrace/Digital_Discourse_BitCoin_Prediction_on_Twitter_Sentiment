# MonkeyCatSunny
This is all the files for my DD course Homework

#######
Most of the code is written with the help of ChatGPT 3.5.

If I can do it, you can do it!!!

#######

if you want to use this crawler, you need to:

First: sign up for Twitter developer account, and subscribe to Twitter API V2 on basic level(100 dollars per month)

Second: install the configparser library if you want to hide you API keys and secrets when sharing code with other researchers

In the config.ini file, do the following, replace all the capitalized part into your own keys and secrets and tokens

[twitterAPI]

api_key = YOUR_OWN_API_KEY
api_key_secret = YOUR_OWN_API_KEY_SECRET

access_token = YOUR_OWN_ACCESS_TOKEN
access_token_secret = YOUR_OWN_ACCESS_TOKEN_SECRET

bearer_token = YOUR_OWN_BEARER_TOKEN

If you have any further questions, let me know

For doing RoBERTa analysis, see the file RoBERTaAnalysis.py

For Merging files, you need MergeCSV.py

For running regressions, please install Anaconda 3(recommended), or install Jupyter and Conda on your editor or IDE. 
For code, see Data_Processing_and_Regression.ipynb
