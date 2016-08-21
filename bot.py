# bot.py, source code for the artBOT behind @art_err_day
#
# by Ian Zapolsky - 3.29.14

import os
import random

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

artists = ['Pablo Picasso', 'Edward Hopper', 'Wassily Kandinsky',
           'Kenneth Noland', 'Alexander Calder', 'Marcel Duchamp',
           'Fritz Glarner', 'Roger de la Fresnaye',
           'Kasimir Malevich', 'Patrick Henry Bruce', 'Renan Ozturk'
           'Fernand Leger', 'Stuart Davis', 'Antoine-Louis Barye',
           'Edward John Poynter', 'Carrie Mae Weems', 'Larry Sultan',
           'Juan Gris', 'Giorgio de Chririco', 'Joan Miro',
           'Stanton McDonald-Wright', 'Charles Sheeler', 'Paul Signac',
           'Alfred Sisley', 'Mark Tansey', 'Simon Hantai', 'Harold Klunder',
           'Ron Martin', 'Frederick B Taylor', 'William R Leigh', 
           'Josef Albers', 'Theo van Doesburg', 'James Ensor', 'Gustav Klimt',
           'Varvara Stepanova', 'Aleksandr Rodchenko', 'Andrew Wyeth',
           'Henri Matisse', 'Paul Cezanne', 'Alexis Gritchenko', 'Charles Demuth',
           'Giorgio de Chirico', 'Chaim Soutine', 'William Glackens',
           'Afro Basaldella', 'Robert Lotiron', 'Maurice Utrillo', 'Max Weber',
           'Julie Dickson',

           # early 20th centry German

           'Lyonel Feininger', 'Paul Klee', 'Oskar Schlemmer', 'Marcel Breuer',
           'Lazlo Moholy-Nagy', 'Alexej Jawlensky', 'Karl Caspar',
           'Christian Rohlfs', 'Karl Schmidt-Rottluff', 
           'Ernst Ludwig Kirchner', 'Lasar Segall', 'Max Beckmann', 
           'Emil Nolde', 'Otto Dix', 'George Grosz', 'Lovis Corinth', 
           'Oskar Kokoschka', 'Felix Nussbaum', 'Egon Schiele', 'Adolf Dehn',

           # Italian futurists

           'Umberto Boccioni', 'Giacomo Balla', 'Luigi Russolo', 'Carlo Carra',
           'Gino Severini', 'Ardengo Soffici', 'Pasqualino Cangiullo',
           "Antonio Sant'Elia", 'Mario Chiattone', 'Mario Sironi',
           'Fortunato Depero', 'Benedetta Cappa Marinetti', 'Enrico Prampolini',
           'Ugo Pozzo', 'Fedele Azari', 'Gerardo Dottori',
           'Alessandro Bruschetti', 'Osvaldo Peruzzi', 'Tullio Crali'

            # Random from Spain
  
           'Robert Delaunay', 'Roy Lichtenstein', 'Robert Rauschenberg', 
           'Diane Arbus', 'Francisco Goya', 'Ferdinand Hodler']

messages = ['check dis', 'yo, peep this', 'dooope', 'siiick',
            'new favorite', 'so artsy', 'so profound', 'so gnarly bra',
            'oh this one hot', 'this is sick', 'really love this one', 
            'discovered this today', 'this is awesome', 'oh snap',
            'this is sick', 'one of a kind', 'i like this', 'OMG', 'incredible',
            'one of my favorites', 'a true original', 'crazy']

hashtags = ['art', 'arterrday', 'paintings', 'beautiful', 'insipiring', 'art',
            'artsy']

def random_hashtag():
  return '#'+hashtags[random.randint(0, (len(hashtags)-1))]

def random_artist():
  return artists[random.randint(0, (len(artists)-1))]

def random_message():
  return messages[random.randint(0, (len(messages)-1))]

# grab one of the first 5 links returned by an image search on the name of
# the artist + "artwork"
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
  msg    = random_message()+' (by '+artist+') '+url+' '+random_hashtag()
  return msg

if __name__ == '__main__':

  # initialize Twitter connection
  t = Twitter(auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET,
                         CONSUMER_KEY, CONSUMER_SECRET))

  msg = random_tweet()
  t.statuses.update(status=msg)

