#import relavant libraries
import pandas as pd
# from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

cos_mov1 = pd.read_csv('pop_key_movies30000.csv')
# print(cos_mov1)

#Helper Functions
# def get_title_from_index(index):
#     return cos_mov1[cos_mov1.index == index]["title"].values[0]

# def get_index_from_title(title):
#     return cos_mov1[cos_mov1.title == title]["index"].values[0]

# def get_combined_features(index):
#     return cos_mov1[cos_mov1.index == index]["combined_features"].values[0]

def get_id_from_index(index):
    return cos_mov1[cos_mov1.index == index]["id"].values[0]

def get_index_from_id(id):
    return cos_mov1[cos_mov1.id == id]["index"].values[0] 

# def get_id_from_title(title):
#     return cos_mov1[cos_mov1["title"] == title]["id"].values[0]

# def get_title_from_id(id):
#     return cos_mov1[cos_mov1["id"] == id]["title"].values[0]


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

# Returns a list of recommended movies from a list of liked movies
def recListMovie(liked_list):
    if not isinstance(liked_list, list):
        liked_list = liked_list.split(",")
    movie_recs = []
    for i in range(len(liked_list)):
        single_movie_recs = recSingleMovie(int(float(liked_list[i])), similarity)
        k=0
        for j in range(len(single_movie_recs)):
            pos = k*(i+1)
            # check in movie is in list
            if single_movie_recs[j] not in movie_recs:
                movie_recs.insert(pos, single_movie_recs[j])
                # if movie is in list, update position
                k=k+1
    return movie_recs

# # Test recListMovie function
# liked_list = [315946, 194079, 315946]
# movie100 = recListMovie(liked_list)
# for x in movie100:
#     print(x)