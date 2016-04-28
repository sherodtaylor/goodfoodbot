from web import routes
from flask import Flask
from os import environ


def run_app():
  app = Flask(__name__)
  routes.setup_routes(app)
  print 'Port: %s' % environ.get('PORT')
  print 'Secret: %s' % environ.get('YELP_CONSUMER_SECRET')
  print environ
  app.run(port=environ.get('PORT'), host='0.0.0.0')



