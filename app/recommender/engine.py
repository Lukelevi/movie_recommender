from app.models import get_all_movies, get_movie_by_genre, find_index_of_movie
#AI Part
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def find_index_of_movie(title: str, all_movies: list, exclude_title=None):
    '''Retrieves the index of a number'''
    title = title.lower()

    for idx, movie in enumerate(all_movies):
        if movie["title"].lower() == title:
            return idx
    return None # or -1

def get_recommendations(title):
    '''...'''
    movies = get_all_movies()

    list_of_movies = [movie["description"] for movie in movies]

    idx = find_index_of_movie(title, list_of_movies)
    if not movies:
        return []
    
    #Initialize TfidfVectorizer()
    vectorizer = TfidfVectorizer() #term frequency inverse-document frequency
    #Fit and transform the documents toTF-IDF vectors: Returns <class list>
    tfidf_matrix = vectorizer.fit_transform(list_of_movies)
    
    #Claculate cosine similarity between the first document and all others
    #tfidf_matrix[0:1] selects the first document's vector
    #tfidf_matrix selects all document vectors
    cosine_similarities = cosine_similarity(
        tfidf_matrix[idx:idx + 1],
        tfidf_matrix)[0] #flatten?
    
    
    similar_indices = "??? should return a list (iterable)"

    recommendations = [movies[i] for i in similar_indices]


    ###SEARCH MOVIEBASED ON DESCRIBING THENTHE APP RECOMMEND MOVIES THAT HAVE A SIMILAR DESCRIPTION CO-JONED WITH GENRE FOR ACCURACY