# -*- coding: utf-8 -*-
"""MLRecommender

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1pXC1ma0NRL9RaaigEF-616BnizUhzpIp
"""

#import relavant libraries
import pandas as pd
# from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#Reading from github link
# url = 'https://raw.githubusercontent.com/si0107/ML_Movie_Recommender/dataset/pop_key_movies4500.csv'
# cos_mov1 = pd.read_csv(url)

cos_mov1 = pd.read_csv('pop_key_movies.csv')
#cos_mov1.head()

#Helper Functions

# Index --> Title
# def get_title_from_index(index):
#     return cos_mov1[cos_mov1.index == index]["title"].values[0]

# # Title --> Index
# def get_index_from_title(title):
#     return cos_mov1[cos_mov1.title == title]["index"].values[0]

# # Index --> Combined Features
# def get_combined_features(index):
#     return cos_mov1[cos_mov1.index == index]["combined_features"].values[0]

# Index --> Id
def get_id_from_index(index):
    return cos_mov1[cos_mov1.index == index]["id"].values[0]

# Id --> Index
def get_index_from_id(id):
    return cos_mov1[cos_mov1.id == id]["index"].values[0]

vectorizer = TfidfVectorizer()
feature_vectors = vectorizer.fit_transform(cos_mov1["combined_features"].values.astype('U'))
similarity = cosine_similarity(feature_vectors)

#Returns a list of top 10 recommended movies
def recSingleMovie(title, similarity):
    id = get_index_from_id(title)
    recs = list(enumerate(similarity[id]))
    sorted_recs = sorted(recs,key=lambda x:x[1],reverse=True)
    sorted_recs.pop(0) #remove the movie itself from the list
    i=0
    top_recs = []
    for element in sorted_recs:
        top_recs.append(get_id_from_index(element[0]))
        i=i+1
        if i>9:
            break
    return top_recs

#returns a list of recommended movies from a list of liked movies
def recListMovie(liked_list):  
  movie_recs = []
  for i in range(len(liked_list)):
    #check if movie is in dataset
    if liked_list[i] in cos_mov1.id.values:
      single_movie_recs = recSingleMovie(liked_list[i], similarity)
      k=0
      for j in range(len(single_movie_recs)):
        pos = k*(i+1)
        # check in movie is in movie_recs or liked list
        if (single_movie_recs[j] not in movie_recs) and (single_movie_recs[j] not in liked_list):
          movie_recs.insert(pos, single_movie_recs[j])
          # if movie is in list, update position
          k=k+1
  return movie_recs

"""**Test Functions**"""

# Test with titles
# 'Frankenstein', 'Batman', 'Young Frankenstein'
# liked_list = ['The Bee Movie', 'Frankenstein', 'Batman', 'Young Frankenstein']
# movie100 = recListMovie(liked_list)
# for x in movie100:
#      print(x)

# Test recListMovie function
# 'Frankenstein', 'Batman', 'Young Frankenstein'
# liked_list = [42069, 3035, 2661, 3034]
# movie100 = recListMovie(liked_list)
# for x in movie100:
#     print(x)