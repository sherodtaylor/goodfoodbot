FROM heroku/python

RUN mkdir /app/nltk_data
ENV NLTK_DATA /app/nltk_data
RUN pip install -r requirements.txt
RUN python -m textblob.download_corpora
