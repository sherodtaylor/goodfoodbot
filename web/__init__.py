from web import routes
from flask import Flask

def run_app():
  app = Flask(__name__)
  routes.setup_routes(app)
  app.run()



