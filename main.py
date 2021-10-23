from searchtweets import load_credentials, collect_results, gen_rule_payload

# twitter part

# load_credentials(filename="./search_tweets_creds_example.yaml",
#                  yaml_key="search_tweets_premium",
#                  env_overwrite=False)


premium_search_args = load_credentials(filename="./search_tweets_creds.yaml",
                 yaml_key="search_tweets_premium",
                 env_overwrite=False)

rule = gen_rule_payload("from:orangebook_", results_per_call=10) # testing with a sandbox account
print(rule)


tweets = collect_results(rule,
                         max_results=10,
                         result_stream_args=premium_search_args) # change this if you need to

# [print(tweet.all_text, end='\n\n') for tweet in tweets[0:10]]


# unsplash part

import requests
import textwrap
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO


def linkFetch():
    query = "office"
    orientation = "squarish"
    url = "https://api.unsplash.com/photos/random?topics=spirituality&content_filter=high&query=people&orientation=squarish&client_id=4PpAlHOuRvO4mse8lIdiTVGUcKUgpNKHVcVSHReIhP0"
    response = requests.get(url, params=query)
    data = response.json()["urls"]["regular"]
    return data

img_url = linkFetch()
response = requests.get(img_url)
img = Image.open(BytesIO(response.content))
width, height = img.size
print('img.width', width, 'img.height', height)
x, y = (width/2, height-height/2)
edited_img = ImageDraw.Draw(img)
fnt = ImageFont.truetype("Ubuntu-R.ttf", 25)
text = tweets[3].all_text
words_cnt = len(tweets)
print(words_cnt)
# text = "Hello world"
# TODO: add new line in text if it is too long 
w, h = fnt.getsize(text)
print('w', w, 'h', h)
if w > 400:
    w = w/2
    parts = round(w/(width/3))
    text_line_parts = text.split() #textwrap.wrap(text, parts)
    chunks = [text_line_parts[x:x+9] for x in range(0, len(text_line_parts), 9)]
    print(chunks)

for line in chunks:
    edited_img.rectangle((x-5-w/2, y-5, x + 5 + w/2, y + 5 + h), fill='grey')
    edited_img.text((x-w/2,y), ' '.join(line), font=fnt, fill="white", align="center")
    y+=60

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