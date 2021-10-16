from searchtweets import load_credentials, collect_results, gen_rule_payload

# load_credentials(filename="./search_tweets_creds_example.yaml",
#                  yaml_key="search_tweets_ent_example",
#                  env_overwrite=False)


premium_search_args = load_credentials(filename="./search_tweets_creds.yaml",
                 yaml_key="search_tweets_premium",
                 env_overwrite=False)

rule = gen_rule_payload("from:orangebook_", results_per_call=10) # testing with a sandbox account
print(rule)


tweets = collect_results(rule,
                         max_results=10,
                         result_stream_args=premium_search_args) # change this if you need to

[print(tweet.all_text, end='\n\n') for tweet in tweets[0:10]]



# install searchtweets
# pip install searchtweets


# apply for dev account and create app
# https://developer.twitter.com/apps
# take key and private key and add them to credentials file 

# create 30-day or full archive dev environments
# https://developer.twitter.com/en/account/environments


# grab the endpoint link
# https://developer.twitter.com/en/docs/twitter-api/premium/search-api/overview
# https://api.twitter.com/1.1/tweets/search/30day/my_env_name.json   (replace my_env_name with the one you created in your dev environment)