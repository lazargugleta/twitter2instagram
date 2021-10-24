from searchtweets import load_credentials, collect_results, gen_rule_payload

# twitter part

# load_credentials(filename="./search_tweets_creds_example.yaml",
#                  yaml_key="search_tweets_premium",
#                  env_overwrite=False)


premium_search_args = load_credentials(filename="./search_tweets_creds.yaml",
                 yaml_key="search_tweets_premium",
                 env_overwrite=False)
twitter_username = 'orangebook_'
rule = gen_rule_payload("from:{}".format(twitter_username), results_per_call=10) # testing with a sandbox account


tweets = collect_results(rule,
                         max_results=10,
                         result_stream_args=premium_search_args) # change this if you need to



def reduce_opacity(im, opacity):
    """Returns an image with reduced opacity."""
    assert opacity >= 0 and opacity <= 1
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    else:
        im = im.copy()
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im

# unsplash part

import requests
import textwrap
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from io import BytesIO


def linkFetch():
    query = "office"
    orientation = "squarish"
    # set different topics, query and your client_id for unspash API request
    client_id = '' # add your client id from unsplash dev page
    url = "https://api.unsplash.com/photos/random?topics=spirituality&content_filter=high&query=people&orientation=squarish&client_id={}".format(client_id)
    response = requests.get(url, params=query)
    data = response.json()["urls"]["regular"]
    id = response.json()["id"]
    users_name = response.json()["user"]["name"]
    return data, users_name

img_url, users_name = linkFetch()
response = requests.get(img_url)
img = Image.open(BytesIO(response.content))
width, height = img.size
img.save("randOrig.jpg")

# reduce brighness
enhancer = ImageEnhance.Brightness(img)
img = enhancer.enhance(0.6)

edited_img = ImageDraw.Draw(img)
fnt = ImageFont.truetype("Ubuntu-R.ttf", 45)
# first tweet from last ten, but can make a loop and do this multiple times for different tweets
text = tweets[0].all_text
# text = "It always looks simple when you are not invested personally and are just watching from outside."
words_cnt = len(text.split(' '))
w, h = fnt.getsize(text)
if w > 400:
    w = w/2
    parts = round(w/(width/3))
    text_line_parts = text.split()
    chunks = [text_line_parts[x:x+7] for x in range(0, len(text_line_parts), 7)]

x, y = (width/2, height-height/2)

# add quotes at the beginning and end of the quote
chunks[0][0] = '"' + chunks[0][0]
chunks[-1][-1] = chunks[-1][-1] + '"'



# im_output.save('darkened-image.jpg')

for line in chunks:
    line_size = fnt.getsize(' '.join(line))
    # text background rectangle (uncomment the line under)
    # edited_img.rectangle((x-line_size[0]/2 -5, y-5, x + line_size[0]/2 +5, y + 5 + h), fill='grey')
    edited_img.text((x-line_size[0]/2,y), ' '.join(line), font=fnt, fill="white", align="center")
    y+=60

# img = img.convert('RGB')
img.save("rand.jpg")

# Instagram filters
# from instafilter import Instafilter
# model = Instafilter("Gingham")
# new_image = model("rand.jpg")
# import cv2
# cv2.imwrite("rand.jpg", new_image)
# img.show()

# further ideas 
# -> figure out the background of your photo and than add text according to it
# -> add background shapes to text

# INSTAGRAM

import os 
# removes cookies If used multiple times to login
import glob
try:
    cookie_del = glob.glob("config/*cookie.json")
    os.remove(cookie_del[0])
except:
    print('No cookies to be deleted')

from instabot import Bot
bot = Bot()
bot.login(username = "motivationtweeter", password = "") # add your accounts username and passwords
# every time after first login
# bot.login()

# credit author of tweet and image
credits = 'Tweet by {} on Twitter.\nPhoto by {} on Unsplash'.format(twitter_username, users_name)

bot.upload_photo("rand.jpg", caption=text + '\n\n' + credits)

# rename file back to original name
os.rename("rand.jpg.REMOVE_ME", "rand.jpg")





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


# instagram
# pip3 install instabot