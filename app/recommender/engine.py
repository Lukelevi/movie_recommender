from app.models import (
    get_all_movies, 
    find_index_of_movie
)
#AI Part
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_recommendations(title):
    '''Retrieves the top 5 movies to recommend'''
    movies = get_all_movies() #Our top movies exist here

    #Movies are in dictionary form (remember that)
    list_of_movies = [movie["description"] for movie in movies]

    idx = find_index_of_movie(title, list_of_movies)
    if not movies:
        return []
    
    #Initialize TfidfVectorizer()
    vectorizer = TfidfVectorizer(stop_words="english") #term frequency inverse-document frequency
    #Fit and transform the documents to TF-IDF vectors: Returns <class list>
    tfidf_matrix = vectorizer.fit_transform(list_of_movies)
    
    #Claculate cosine similarity between the first document and all others
    #tfidf_matrix[0:1] selects the first document's vector
    #tfidf_matrix selects all document vectors
    cosine_similarities = cosine_similarity(    
        tfidf_matrix[idx:idx + 1],
        tfidf_matrix)[0] #flatten?  # Returns (1, n_features(movies in this instance))
    
    
    #Score enumeration
    indexed_scores = list(enumerate(cosine_similarities))

    #Remove itself (recommending the same movie)
    indexed_scores = [pair for pair in indexed_scores if pair[0] != idx] #Zero represents the index of the the tuple

    #Sort by similarity
    indexed_scores = sorted(indexed_scores, key=lambda x: x[1], reverse=True)

    #Pick top N movies (top 5 movies)
    top_indices = [pair[0] for pair in indexed_scores[:5]]

    #Return the actual movie dictionaries
    return [movies[idxx] for idxx in top_indices]

    


    ###SEARCH MOVIEBASED ON DESCRIBING THENTHE APP RECOMMEND MOVIES THAT HAVE A SIMILAR DESCRIPTION CO-JONED WITH GENRE FOR ACCURACY