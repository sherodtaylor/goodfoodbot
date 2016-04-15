from flask import Flask
from flask import request
from bot.chatbot import GoodFoodBot
from textblob import TextBlob
from textblob.np_extractors import ConllExtractor

import requests
import json
import logging


logging.basicConfig(level=logging.DEBUG)

# Train based on the english corpus
app = Flask(__name__)

bot = GoodFoodBot()

extractor = ConllExtractor()

def sendMessage(sender, text):
	response = bot.get_response(text) 

	payload = {
		'message': {
			'text': response
		},
		'recipient': {
			'id': sender
		}
	}
	blob = TextBlob(text, np_extractor=extractor)
	print blob.tags
	print blob.noun_phrases


	params = { 'access_token': 'CAADdh54XfDYBANyqSoTahYD5NYMIFLNk0KoNpiOidVRMzjLO2K9nd88QVoX0EzFGN3mbR3bRA7LlV6DOJynYH5txVWfa2jZBAE1u68HKuIKFFzY5gfEE1R5lATB6MnSyRjq2XFNOCbGcDrN5YpONIwMgBRy9UKwnCz14ZAcQBQdfPYVbkiZBmrSei3rPkQZD'}

	print requests.post("https://graph.facebook.com/v2.6/me/messages", json=payload, params=params).text



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


if __name__ == "__main__":
  app.run()
