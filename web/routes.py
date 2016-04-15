from flask import Flask
from flask import request



app = Flask(__name__)

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
