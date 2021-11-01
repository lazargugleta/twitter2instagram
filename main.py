from searchtweets import load_credentials, gen_request_parameters, ResultStream
from creds import instagram_username, instagram_password, client_id
import os
from instabot import Bot
import requests
import textwrap
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from io import BytesIO

# twitter part

def getTweets(number_of_tweets):

    min_nr_tweets = 10
    if number_of_tweets < 10:
        number_of_tweets += min_nr_tweets

    search_args = load_credentials(
        filename="./search_tweets_creds.yaml",
        yaml_key="search_tweets_v2",
        env_overwrite=True,
    )

    # testing with a sandbox account
    query = gen_request_parameters(
        "from:{}".format(twitter_username), results_per_call = number_of_tweets, granularity=None
    )

    rs = ResultStream(request_parameters=query,
                    max_results=number_of_tweets,
                    **search_args)

    tweets = list(rs.stream())
    number_of_tweets -= min_nr_tweets
    return [tweets[0]["data"][i]["text"] for i in range(0, number_of_tweets)]


# Unsplash

def getImage():
    query = "office"
    orientation = "squarish"
    # set different topics, query and your client_id for unspash API request
    # add your client id from unsplash dev page to creds.py
    url = "https://api.unsplash.com/photos/random?topics=spirituality&content_filter=high&query=people&orientation=squarish&client_id={}".format(
        client_id
    )
    response = requests.get(url, params=query)
    data = response.json()["urls"]["regular"]
    # id = response.json()["id"]
    users_name = response.json()["user"]["name"]
    img = Image.open(BytesIO(requests.get(data).content))

    return img, data, users_name

# Instagram

def loginInstagram():

    # removes cookies If used multiple times to login
    import glob

    try:
        cookie_del = glob.glob("config/*cookie.json")
        os.remove(cookie_del[0])
    except:
        print("No cookies to be deleted")

    # login with username and password
    bot = Bot()
    bot.login(username=instagram_username, password=instagram_password)
    # add your accounts username and passwords to creds.py
    # every time after first login
    # bot.login()
    return bot


def makePost(text, instaBot):
    # get image
    img, img_url, users_name = getImage()
    width, height = img.size

    # reduce brighness
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(0.6)
    edited_img = ImageDraw.Draw(img)
    fnt = ImageFont.truetype("Ubuntu-R.ttf", 45)
    twitter_logo = Image.open("twitter.png")
    unsplash_logo = Image.open("unsplash.png")
    # text = "If you are the smartest person in the room, you are in the wrong room."
    w, h = fnt.getsize(text)
    text_line_parts = text.split()
    if text_line_parts[0] == "RT" and text_line_parts[1][0] == "@":
        text_line_parts = text_line_parts[2:len(text_line_parts)]
        text = " ".join(text_line_parts)

    if w > 400:
        w = w / 2
        parts = round(w / (width / 3))
        chunks = [text_line_parts[x : x + 7] for x in range(0, len(text_line_parts), 7)]

    for chunk in chunks:
        if fnt.getsize(" ".join(chunk))[0] >= (img.width - 50):
            chunks = [text_line_parts[x : x + 6] for x in range(0, len(text_line_parts), 6)]
            break

    # get center
    x, y = (width / 2, height - height / 2)

    # add quotes at the beginning and end of the quote
    chunks[0][0] = '"' + chunks[0][0]
    chunks[-1][-1] = chunks[-1][-1] + '"'
    number_of_chunks = len(chunks)
    y -= int(round(number_of_chunks/2 * 50))

    for line in chunks:
        line_size = fnt.getsize(" ".join(line))
        # text background rectangle (uncomment the line under)
        # edited_img.rectangle((x-line_size[0]/2 -5, y-5, x + line_size[0]/2 +5, y + 5 + h), fill='grey')
        edited_img.text(
            (x - line_size[0] / 2, y),
            " ".join(line),
            font=fnt,
            fill="white",
            align="center",
        )
        y += 60

    # credits at the bottom of the image
    # twitter and unsplash logos for the handles of the authors
    img.paste(twitter_logo, (int(round(x)) - 155, int(round(height))-130), twitter_logo)
    img.paste(unsplash_logo, (int(round(x)) - 157, int(round(height))-70), unsplash_logo)

    # resize font
    fnt = ImageFont.truetype("Ubuntu-R.ttf", 30)
    edited_img.text((int(round(x)) - 100, int(round(height))-125), "@" + twitter_username, font = fnt, fill="white", align="center")
    edited_img.text((int(round(x)) - 100, int(round(height))-65), "@" + users_name, font = fnt, fill="white", align="center")

    img.save("post.jpg")

    # Instagram filters
    # from instafilter import Instafilter
    # model = Instafilter("Gingham")
    # new_image = model("rand.jpg")
    # import cv2
    # cv2.imwrite("rand.jpg", new_image)
    # img.show()

    # credit author of tweet and image
    credits = "Tweet by @{} on Twitter.\nPhoto by {} on Unsplash".format(
        twitter_username, users_name
    )

    instaBot.upload_photo("post.jpg", caption=text + "\n\n" + credits)

    # rename file back to original name
    os.rename("post.jpg.REMOVE_ME", "post.jpg")

twitter_username = input("Enter the twitter username: @")
number_of_tweets = int(input("Enter the number of tweets: "))

texts = getTweets(number_of_tweets)
# flow
instaBot = loginInstagram()
# texts = "We develop low-level addictions to junk that fuels our insecurities: junk information, junk activities, junk friends. Quitting means exposing emotions and triggering weird cravings but the goal is to stay focused on things that add value to your life."
for text in texts:
    print(text)
    makePost(text, instaBot)
print("Script complete check instagram to see the posts {}".format("https://instagram.com/" + instagram_username))


# further ideas
# -> check if the twitter username is written properly
# -> write queries for each of the functions (number of tweets, user to get tweets from, unplash query photo criteria, instagram auto/manual login (if it exists in the creds file))
# -> figure out the background of your photo and than add text according to it
# -> add background shapes to text and personalize it however you like
# -> add tweet and photo authors on the bottom of the photo
# -> filter tweets from keywords (e.g. threads or Retweets)
# -> move text a bit up when it is long // DONE

# HOW TO INSTALL AND USE

# install searchtweets
# pip install searchtweets-v2 


# apply for dev account and create app
# https://developer.twitter.com/apps
# take key and private key and add them to credentials file

# curl command to add bearer token

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
