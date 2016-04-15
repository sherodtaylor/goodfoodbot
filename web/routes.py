from flask import request
import requests
from bot.chatbot import GoodFoodBot
from textblob import TextBlob
from textblob.np_extractors import ConllExtractor
from nltk.corpus import nps_chat

# chatroom = nps_chat.posts('10-19-20s_706posts.xml')

bot = GoodFoodBot()

extractor = ConllExtractor()

def sendMessage(sender, text):
  response = bot.get_response(text) 

  payload = {
    'message': {
      'attachment': {
        'type': 'template',
        'payload': {
          'template_type': 'button',
          'text': 'would you like to book this table?',
          'image': 'http://s3-media1.fl.yelpcdn.com/bphoto/dwXzh1hkhlNIU_as63XbOg/o.jpg',
          'buttons': [
            {
              'type': 'web_url',
              'title': 'yes',
              'url': 'https://f872504b.ngrok.io/api/restaurant'
            },
            {
              'type': 'web_url',
              'title': 'no',
              'url': 'https://f872504b.ngrok.io/api/restaurant'
            }
          ]
        }
      }
    },
    'recipient': {
      'id': sender
    }
  }

  blob = TextBlob(text, np_extractor=extractor)
  print blob.tags

  params = { 'access_token': 'CAADdh54XfDYBANyqSoTahYD5NYMIFLNk0KoNpiOidVRMzjLO2K9nd88QVoX0EzFGN3mbR3bRA7LlV6DOJynYH5txVWfa2jZBAE1u68HKuIKFFzY5gfEE1R5lATB6MnSyRjq2XFNOCbGcDrN5YpONIwMgBRy9UKwnCz14ZAcQBQdfPYVbkiZBmrSei3rPkQZD'}

  print requests.post("https://graph.facebook.com/v2.6/me/messages", json=payload, params=params).text


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
  		messaging_events = request.get_json()['entry'][0]['messaging']
  		print messaging_events
  		for event in messaging_events:
  			if 'message' in event:
  				if 'text' in event['message']:
  					sendMessage(event['sender']['id'], event['message']['text'])
  		return 'okay', 200
