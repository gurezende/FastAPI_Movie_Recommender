import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Update the DATABASE_URL with your actual PostgreSQL credentials
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://recommender_user:admin@localhost/movie_recommender")

# Create the engine for postgresql
engine = create_engine(DATABASE_URL)

# Create the local session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
