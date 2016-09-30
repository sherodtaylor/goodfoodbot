FROM heroku/python

RUN pip install -r requirements.txt

RUN python -m spacy.en.download --force all

RUN python -c "import spacy; spacy.load('en'); print('OK')"
