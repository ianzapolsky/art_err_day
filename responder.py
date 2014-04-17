# bot.py, source code for the artBOT behind @art_err_day
#
# by Ian Zapolsky - 3.29.14

import os
import random
import time

from apiclient.discovery import build
from twitter import Twitter, OAuth, TwitterHTTPError

# screen name of the twitter account this bot will be operating under
BOT_NAME = 'art_err_day'

# Twitter API authentication
OAUTH_TOKEN     = os.environ['OAUTH_TOKEN']
OAUTH_SECRET    = os.environ['OAUTH_SECRET']
CONSUMER_KEY    = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']

# Google API authentication
GOOGLE_DK = os.environ['GOOGLE_DK']
GOOGLE_CX = os.environ['GOOGLE_CX']

# List of artists we want in the collection
artists = ['Pablo Picasso', 'Edward Hopper', 'Wassily Kandinsky',
           'Kenneth Noland', 'Alexander Calder', 'Marcel Duchamp',
           'Fritz Glarner', 'Adolf Dehn', 'Roger de la Fresnaye',
           'Kasimir Malevich', 'Patrick Henry Bruce', 'Renan Ozturk'
           'Fernand Leger', 'Stuart Davis', 'Antoine-Louis Barye',
           'Edward John Poynter', 'Carrie Mae Weems', 'Larry Sultan',
           'Paul Klee', 'Juan Gris', 'Giorgio de Chririco', 'Joan Miro',
           'Stanton McDonald-Wright', 'Charles Sheeler', 'Paul Signac',
           'Alfred Sisley', 'Mark Tansey', 'Simon Hantai', 'Harold Klunder',
           'Ron Martin', 'Frederick B Taylor', 'William R Leigh', 
           'Josef Albers', 'Theo van Doesburg', 'James Ensor', 'Gustav Klimt',
           'Umberto Boccioni', 'Varvara Stepanova', 'Aleksandr Rodchenko']

# List of messages
messages = ['check dis', 'yo, peep this', 'dooope', 'siiick',
            'new favorite', 'so artsy', 'so profound', 'so gnarly bra',
            'oh this one hot', 'this is sick']

def random_artist():
  return artists[random.randint(0, (len(artists)-1))]

def random_message():
  return messages[random.randint(0, (len(messages)-1))]

def random_link(artist):
  service = build('customsearch', 'v1', developerKey=GOOGLE_DK)
  result = service.cse().list(
      q          = artist+' artwork',
      searchType = 'image',
      imgSize    = 'xlarge',
      cx         = GOOGLE_CX
  ).execute()
  return result['items'][random.randint(0,5)]['link']

def random_tweet():
  artist = random_artist()
  url    = random_link(artist)
  msg    = random_message()+' (by '+artist+') '+url
  return msg

# return all tweets mentioning @BOT_NAME that have been created since latest_id
def fetch_unseen_mentions(latest_id):
  return t.search.tweets(q='@'+BOT_NAME, result_type='recent', since_id=latest_id)['statuses']

# return the id of the latest tweet mentioning @BOT_NAME
def fetch_latest_id():
  return t.search.tweets(q='@'+BOT_NAME, result_type='recent', count=1)['statuses'][0]['id']


if __name__ == '__main__':

  # initialize Twitter connection
  t = Twitter(auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET,
                         CONSUMER_KEY, CONSUMER_SECRET))

  # read in the latest id from the last check
  f = open('.latest_id', 'r')
  latest_id = f.read().rstrip()
  f.close()

  # check for unseen tweets since the latest id
  results = fetch_unseen_mentions(latest_id)

  # if we got any tweets, reply to them
  if results:
    for tweet in reversed(results):

      tweeter  = tweet['user']['screen_name']
      artist = random_artist()
      url    = random_link(artist)
      msg    = '@'+tweeter+' '+random_tweet()
      t.statuses.update(status=msg)
      
      latest_id = str(tweet['id'])

  # write the new latest_id to the file
  f = open('.latest_id', 'w')
  f.write(latest_id)
  f.close()


