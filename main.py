from searchtweets import load_credentials, collect_results, gen_rule_payload

# twitter part

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


# unsplash part

import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO


def linkFetch():
    query = "office"
    orientation = "squarish"
    url = "https://api.unsplash.com/photos/random?topics=spirituality&content_filter=high&query=people&orientation=squarish&client_id=4PpAlHOuRvO4mse8lIdiTVGUcKUgpNKHVcVSHReIhP0"
    response = requests.get(url, params=query)
    # print(response.json()["results"]["urls"])
    data = response.json()["urls"]["regular"]
    return data

img_url = linkFetch()
response = requests.get(img_url)
img = Image.open(BytesIO(response.content))
width, height = img.size
x, y = (width/4, height-height/2)
xx, yy = (width/4, height-height/2)
edited_img = ImageDraw.Draw(img)
fnt = ImageFont.truetype("Ubuntu-R.ttf", 30)
text = tweets[1].all_text
w, h = fnt.getsize(text)
edited_img.rectangle((x-5, y-5, x + 5 + w, y + 5 + h), fill='grey')
edited_img.text((x,y), text, font=fnt, fill="white", align="center")
img.show()


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


# unsplash
# register for unsplash developers
# https://unsplash.com/developers

# register app
# https://unsplash.com/oauth/applications

# make requests using rest api