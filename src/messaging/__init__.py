import requests
import os

def send_message(payload):
  params = { 'access_token': os.environ.get('FB_ACCESS_TOKEN') }
  return requests.post("https://graph.facebook.com/v2.6/me/messages", json=payload, params=params)

