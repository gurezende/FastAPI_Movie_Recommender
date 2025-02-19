import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Update the DATABASE_URL with your actual SQLite credentials
DATABASE_URL = "sqlite:///movie_recommender.db"

# Create the engine for sqlite
engine = create_engine(
    DATABASE_URL,
    connect_args= {"check_same_thread": False} #It allows multiple threads to use the same database connection, which SQLite does not allow by default.
    )

# Create the local session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

'''
Python file to create database connection and session
'''