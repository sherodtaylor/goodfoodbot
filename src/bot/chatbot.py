from chatterbot import ChatBot
from os import path


class GoodFoodBot: 
  def __init__(self):
    self.bot = ChatBot('Good Food Bot')

    print 'start training'

    # Train based on the english conversations corpus

    print 'finished training'

  def train_bot(self):
    chunks = self.get_chunks(self.clean_dataset, 100)
    print 'start chunk training'
    for chunk, i in chunks:
      self.bot.train(chunk)
      print 'finished chunk %s' % i


    print 'finished training with movie_lines'
  def clean_dataset(self):
    n = path.join(path.dirname(__file__), 'data/movie_lines.txt')
    file = open(n, 'r')
    array = file.read().split('\n')
    mapped_arr = map(lambda txt: txt.split(' +++$+++ ')[-1:][0], array[0:1000])
    return mapped_arr

  def format_data(self, arr):
    return map(lambda txt: txt.split(' +++$+++ ')[-1:][0], arr)

  def get_response(self, text):
    return self.bot.get_response(text) 

  def get_chunks(self, arr, n):
    # Declare some empty lists
    chunk = []
    chunks = []
   
    # Step through the data n elements
    # at a time
    for x in range(0, len(arr), n):
      # Extract n elements
      chunk = arr[x:x+n]
      # Add them to list
      chunks.append(chunk)
   
    # Return the new list
    return chunks