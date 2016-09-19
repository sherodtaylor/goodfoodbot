from web import run_app
import logging
import nltk


logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
  nltk.download()
  run_app()