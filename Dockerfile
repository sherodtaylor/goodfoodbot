FROM heroku/python

RUN mkdir /app/nltk_data
ENV NLTK_DATA /app/nltk_data
RUN python -m textblob.download_corpora
