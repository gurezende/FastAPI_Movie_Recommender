# Imports
import pandas as pd
from sqlalchemy.orm import Session
from myapp.database import SessionLocal, engine
from myapp.models import Base, Movie, Rating

# Create if not exists
Base.metadata.create_all(bind=engine)

# Load datasets
movies_path = "./data/u.item"  # Adjust this if your dataset is stored elsewhere
ratings_path = "./data/u.data"

# Load Movies with Pandas
colnames = ['movie_id', 'title', 'release_date','unknown', 'action', 'adventure', 'animation', 'children',
            'comedy', 'crime', 'documentary', 'drama', 'fantasy','filmnoir', 'horror', 'musical','mystery',
            'romance', 'scifi', 'thriller', 'war', 'western']

movies_df = pd.read_csv(movies_path, sep="|", header=None, usecols=[0,1,2,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23], names=colnames)

# Load Ratings with Pandas
ratings_df = pd.read_csv(ratings_path, sep="\t", header=None, usecols=[0,1,2], names=["user_id", "movie_id", "rating"])

# Insert movies into PostgreSQL
def insert_movies():

    # Open local session with the database
    with SessionLocal() as session:
        movies = [
            Movie(movie_id=str(row["movie_id"]), title=row["title"], release_date=row["release_date"], unknown=row["unknown"],
                  action=row["action"], adventure=row["adventure"], animation=row["animation"], children=row["children"],
                  comedy=row["comedy"],crime=row["crime"], documentary=row["documentary"], drama=row["drama"], fantasy=row["fantasy"],
                  filmnoir=row["filmnoir"], horror = row["horror"], musical= row["musical"], mystery=row["mystery"], romance=row["romance"],
                  scifi=row["scifi"], thriller=row["thriller"], war= row["war"], western= row["western"])
            # Add movies
            for _, row in movies_df.iterrows()
        ]
        #Save and commit
        session.bulk_save_objects(movies)
        session.commit()
    print("Movies inserted successfully.")

# Insert ratings into PostgreSQL
def insert_ratings():
    # Open local session with the database
    with SessionLocal() as session:
        ratings = [
            Rating(
                user_id=str(row["user_id"]),
                movie_id=str(row["movie_id"]), 
                rating=float(row["rating"]) )
            # Add ratings                   
            for _, row in ratings_df.iterrows()
        ]
        # Save and commit
        session.bulk_save_objects(ratings)
        session.commit()
    print("Ratings inserted successfully.")

# Run data insertion
if __name__ == "__main__":
    insert_movies()
    insert_ratings()