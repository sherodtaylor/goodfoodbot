import requests
import messaging
from messaging import templates

from flask import request

from spacy.en import English
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
import json
from os import environ
from spacy.parts_of_speech import ADJ, NOUN

nlp = English()

def handle_events(messaging_events):
  for event in messaging_events:
    print event
    if 'message' in event:
      if 'text' in event.get('message', {}):
        handle_message(event['sender']['id'], event['message']['text'])


def handle_message(sender, text):
  text_doc = en_nlp(text);

  location = 'New York'
  search_terms = ' '.join([tok.text for tok in text_doc if tok.pos == ADJ or tok.pos == NOUN])

  try:
    location = next(ent.text for ent in list(text_doc.ents) if ent.label_ == 'GPE')
  except:
    print 'Error'

  results = search_yelp(location, search_terms)
  print results

  elements = []
  print results.businesses
  if len(results.businesses) > 0:
    for business in list(results.businesses):
      print business
      buttons = []

      restaurant = {
        'buttons': buttons,
        'title': business.name,
        'subtitle': business.snippet_text
      }


      if business.image_url is not None:
        restaurant.image_url = business.image_url.replace('ms.jpg', 'l.jpg')

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

def search_yelp(location, search_terms):
  auth = Oauth1Authenticator(
    consumer_key=environ.get('YELP_CONSUMER_KEY'),
    consumer_secret=environ.get('YELP_CONSUMER_SECRET'),
    token=environ.get('YELP_TOKEN'),
    token_secret=environ.get('YELP_TOKEN_SECRET')
  )

  terms = reduce(lambda prev, curr: prev + ' ' + curr, nouns, ''),
  print terms
  client = Client(auth)
  return client.search(location, **{
    'term': search_terms,
    'limit': 3,
    'category_filter': 'restaurants'
  });

def setup_routes(app):
  @app.route("/")
  def hello():
  	return 'hello'

  @app.route("/test")
  def test():

    return 'hi', 200



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
