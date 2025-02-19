from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class ClickStats(Base):
    __tablename__ = "click_stats"
    
    # Using movie_id as a string (you can change to Integer if your movie ids are numeric)
    movie_id = Column(String, primary_key=True, index=True)
    title = Column(String, unique=True, index=True, default="")
    recommendations_shown = Column(Integer, default=0)
    clicks = Column(Integer, default=0)

class Movie(Base):
    __tablename__ = "movies"

    # Table columns
    movie_id= Column(String, primary_key=True, index=True)
    title= Column(String, default="", index=True)
    release_date= Column(String, default="")
    unknown= Column(Integer, default=0)
    action= Column(Integer, default=0)
    adventure= Column(Integer, default=0)
    animation= Column(Integer, default=0)
    children = Column(Integer, default=0)
    comedy  = Column(Integer, default=0)
    crime  = Column(Integer, default=0)
    documentary  = Column(Integer, default=0)
    drama  = Column(Integer, default=0)
    fantasy  = Column(Integer, default=0)
    filmnoir  = Column(Integer, default=0)
    horror  = Column(Integer, default=0)
    musical  = Column(Integer, default=0)
    mystery = Column(Integer, default=0)
    romance = Column(Integer, default=0)
    scifi = Column(Integer, default=0)
    thriller = Column(Integer, default=0)
    war = Column(Integer, default=0)
    western = Column(Integer, default=0)


class Rating(Base):
    __tablename__ = "ratings"

    # Table columns
    user_id = Column(String, primary_key=True, index=True)
    movie_id = Column(String, primary_key=True, index=True)
    rating = Column(Float, default=0)