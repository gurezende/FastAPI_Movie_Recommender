# Imports
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from myapp.database import engine

# Function to load data from the SQLite database
def load_data():
    """
    Loads movies and ratings data from SQLite into Pandas DataFrames.
    """
    # Load movies from the movies table
    movies_df = pd.read_sql("SELECT * FROM movies", con=engine)
    # Load ratings from the ratings table
    ratings_df = pd.read_sql("SELECT * FROM ratings", con=engine)
    
    return ratings_df, movies_df

# Function to get movies list
def get_movies_list():
    """
    Returns a list of movie titles.
    """
    # Load movies from the movies table
    movies_df = pd.read_sql("SELECT DISTINCT(title) FROM movies", con=engine)
    # Convert the DataFrame to a list of movie titles
    movies_list = movies_df.values.flatten()
    
    return movies_list

# Calculate cosine similarity matrix
def create_similarity_matrix(ratings):
    # Create a pivot table with movies as rows and users as columns
    movie_matrix = ratings.pivot_table(index="movie_id", columns="user_id", values="rating").fillna(0)
    
    # Compute cosine similarity between movies
    similarity = cosine_similarity(movie_matrix)
    
    # Create a DataFrame for easier lookup
    similarity_df = pd.DataFrame(similarity, index=movie_matrix.index, columns=movie_matrix.index)
    
    return similarity_df

# Make recommendations
def get_recommendations(movie_title, movies, similarity_df, top_n=4):
    """
    Given a movie title, return top_n recommended movies.
    """
    # Map movie title to movie_id
    movie_lookup = movies.set_index("title")["movie_id"].to_dict()
    
    if movie_title not in movie_lookup:
        return "Movie not found."
    
    # Lookup movie_id for the given movie name
    movie_id = movie_lookup[movie_title]
    
    if movie_id not in similarity_df.index:
        return "Movie not found."
    
    # Retrieve similarity scores for the given movie
    scores = similarity_df[movie_id]
    
    # Sort scores in descending order. Exclude the movie itself.
    sorted_scores = scores.sort_values(ascending=False)
    similar_movie_ids = sorted_scores.index[1:top_n+1].tolist()
    
    # Map movie_ids back to movie titles for the recommendations
    id_to_title = movies.set_index("movie_id")["title"].to_dict()
    recommendations = [id_to_title[mid] for mid in similar_movie_ids if mid in id_to_title]
    
    return recommendations

# Test
# if __name__ == "__main__":
#     ratings, movies = load_data()
#     similarity_df = create_similarity_matrix(ratings)
#     test_movie = str.lower("back to the future")  # Change this to a title that exists in your database
#     recs = get_recommendations(test_movie, ratings, movies, similarity_df)
#     print(f"Recommendations for '{test_movie}': {recs}")

