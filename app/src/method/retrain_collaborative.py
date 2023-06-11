import tensorflow as tf
import numpy as np
import pandas as pd
import tensorflow as tf
from typing import Dict, Text
import tensorflow_recommenders as tfrs 
import os

class BookLensModel(tfrs.Model):
  # We derive from a custom base class to help reduce boilerplate. Under the hood,
  # these are still plain Keras Models.
 
  def __init__(
      self,
      user_model: tf.keras.Model,
      book_model: tf.keras.Model,
      task: tfrs.tasks.Retrieval):
    super().__init__()
 
    # Set up user and book representations.
    self.user_model = user_model
    self.book_model = book_model
 
    # Set up a retrieval task.
    self.task = task
 
  def compute_loss(self, features: Dict[Text, tf.Tensor], training=False) -> tf.Tensor:
    # Define how the loss is computed.
 
    user_embeddings = self.user_model(features["user_id"])
    book_embeddings = self.book_model(features["book_title"])
 
    return self.task(user_embeddings, book_embeddings)

# convert them to tf datasets
def data(ratings_df, books_df):
    ratings_df["ISBN"] = ratings_df["ISBN"].astype(str)
    books_df["ISBN"] = books_df["ISBN"].astype(str)
    ratings_df = ratings_df[['ISBN', 'UserID']]
    books_df = books_df[['ISBN', 'BookTitle']]
    ratings = pd.merge(ratings_df, books_df, on='ISBN')
    ratings = ratings[['BookTitle', 'UserID']].reset_index(drop=True)
    books = books_df[['ISBN', 'BookTitle']]
    books['Item-ID'] = books['ISBN'].astype('category').cat.codes + 1
    books = books[['Item-ID', 'BookTitle']].reset_index(drop=True)
    ratings.rename(columns = {'BookTitle': 'book_title', 'UserID' : 'user_id'}, inplace=True)
    books.rename(columns = {'BookTitle': 'book_title', 'Item-ID' : 'item_id'}, inplace=True)
    # print(ratings_df)
    # print(books_df)
    ratings = tf.data.Dataset.from_tensor_slices(dict(ratings))
    books = tf.data.Dataset.from_tensor_slices(dict(books))
    # Select the basic features.
    return ratings, books

def train(ratings, books):
    ratings, books = data(ratings, books)
    ratings = ratings.map(lambda x: {
        "book_title": x["book_title"],
        "user_id": x["user_id"]
    })
    books = books.map(lambda x: x["book_title"])
    user_ids_vocabulary = tf.keras.layers.IntegerLookup(mask_token=None)
    user_ids_vocabulary.adapt(ratings.map(lambda x: x["user_id"]))
    
    
    book_titles_vocabulary = tf.keras.layers.StringLookup(mask_token=None)
    book_titles_vocabulary.adapt(books)
    # Define user and book models.
    user_model = tf.keras.Sequential([
        user_ids_vocabulary,
        tf.keras.layers.Embedding(user_ids_vocabulary.vocabulary_size(), 64)
    ])
    book_model = tf.keras.Sequential([
        book_titles_vocabulary,
        tf.keras.layers.Embedding(book_titles_vocabulary.vocabulary_size(), 64)
    ])
    
    # Define your objectives.
    task = tfrs.tasks.Retrieval(metrics=tfrs.metrics.FactorizedTopK(
        books.batch(128).map(book_model)
    )
    )
    # Create a retrieval model.
    model = BookLensModel(user_model, book_model, task)
    model.compile(optimizer=tf.keras.optimizers.Adagrad(0.5))
    
    # Train for 3 epochs.
    model.fit(ratings.batch(4096), epochs=3)
        # Use brute-force search to set up retrieval using the trained representations.
    index = tfrs.layers.factorized_top_k.BruteForce(model.user_model)
    index.index_from_dataset(books.batch(100).map(lambda title: (title, model.book_model(title))))
    path = os.path.join('./data', "model")
    # Save the index.
    tf.saved_model.save(index, path)