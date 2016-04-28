import requests
import messaging
from messaging import templates

from flask import request
from bot.chatbot import GoodFoodBot
from textblob import TextBlob
from textblob.np_extractors import ConllExtractor

from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
import json
from os import environ

bot = GoodFoodBot()
extractor = ConllExtractor()

def handle_events(messaging_events):
  for event in messaging_events:
    print event
    if 'message' in event:
      if 'text' in event.get('message', {}):
        handle_message(event['sender']['id'], event['message']['text'])


def handle_message(sender, text):
  response = bot.get_response(text) 
  blob = TextBlob(text, np_extractor=extractor)
  for noun in blob.noun_phrases:
    print blob.noun_phrases

  for word, tag in blob.tags:
    print word + ' --> ' + tag

  if len(blob.noun_phrases) == 0:
    return 'okay', 200

  results = search_yelp(blob.noun_phrases)
  print results

  elements = []
  print results.businesses
  if len(results.businesses) > 0:
    for business in list(results.businesses):
      print business
      buttons = []

      elements.append({
        'buttons': buttons,
        'title': business.name,
        'subtitle': business.snippet_text  ,
        'image_url': business.image_url.replace('ms.jpg', 'l.jpg')
      })

      print business.__dict__

      if business.reservation_url is not None:
        buttons.append(templates.button('web_url', 'reserve', business.reservation_url))

      if business.mobile_url is not None:
        buttons.append(templates.button('web_url', 'visit yelp', business.mobile_url))

    message = templates.generic_template(sender, {
      'template_type': 'generic',
      'elements': elements
    })
  else:
    message = templates.button_template(sender, 'Do you want to checkout yelp?', buttons)

  print messaging

  print messaging.send_message(message).text
  return 'okay', 200

def search_yelp(nouns):
  auth = Oauth1Authenticator(
    consumer_key=environ.get('YELP_CONSUMER_KEY'),
    consumer_secret=environ.get('YELP_CONSUMER_SECRET'),
    token=environ.get('YELP_TOKEN'),
    token_secret=environ.get('YELP_TOKEN_SECRET')
  )

  terms = reduce(lambda prev, curr: prev + ' ' + curr, nouns, ''),
  print terms
  client = Client(auth)
  return client.search('New York, NY', **{
    'term': nouns[0],
    'limit': 3,
    'category_filter': 'restaurants'
  });

def setup_routes(app):
  @app.route("/")
  def hello():
  	return 'hello'

  @app.route("/webhook/", methods=['POST', 'GET'])
  def webhook():
  	if request.method == 'GET':
  		if request.args.get("hub.verify_token") == "verified_sherod":
  			return request.args.get("hub.challenge")

  		return "Error, wrong validation token"
  	else:
  		messaging_events = request.get_json().get('entry', [])[0].get('messaging', [])
  		handle_events(messaging_events)
  		return 'okay', 200
