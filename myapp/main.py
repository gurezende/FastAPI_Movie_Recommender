from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from myapp.database import engine, SessionLocal #import local session and engine
from myapp.models import Base, ClickStats, Movie, Rating #import models (table schemas)
from myapp import recommender #import recommender system from recommender.py
from myapp.schemas import MovieCreate #get MovieCreate for the ability to add new movies

# Create app instance
app = FastAPI(title="Movie Recommender API")

# Dependency to get DB session for endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Load the dataset and precompute the similarity matrix once at startup
ratings, movies = recommender.load_data()
similarity_df = recommender.create_similarity_matrix(ratings)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Movie Recommender API"}

# Recommendation endpoint
@app.get("/recommend/")
def get_recommendations(movie: str, db: Session = Depends(get_db)):
    # Get the recommendations
    """
    Get movie recommendations given a movie title.

    Args:
        movie (str): movie title to get recommendations for
        db (Session, optional): database session. Defaults to Depends(get_db).

    Returns:
        dict: containing the movie title and a list of recommendations
    """
    rec_titles = recommender.get_recommendations(movie, movies, similarity_df)
    
    # queried_movie_id = movies[movies['title'] == movie]['movie_id'].values[0]
    
    # Empty list to store the recommendations
    recommendations = []
    
    for rec_title in rec_titles:
        # Retrieve movie_id for the recommended movie from the movies dataframe
        rec_movie_id = movies[movies['title'] == rec_title]['movie_id'].values[0]
        
        # Update the recommendation
        # s_shown counter for this movie
        record = db.query(ClickStats).filter(ClickStats.movie_id == str(rec_movie_id)).first()
        if not record:
            record = ClickStats(movie_id=str(rec_movie_id), 
                                title = rec_title,
                                recommendations_shown=1, 
                                clicks=0)
            db.add(record)
        else:
            record.recommendations_shown += 1
        db.commit()
        
        # Append the recommendation details (movie_id and title)
        recommendations.append({"movie_id": str(rec_movie_id), "title": rec_title})
    
    return {"movie": movie, "recommendations": recommendations}

# Click tracking endpoint
@app.post("/click/")
def update_click(movie_id: str, db: Session = Depends(get_db)):
    """
    Updates the click count for a given movie_id.

    Args:
        movie_id (str): the movie_id to update the click count for
        db (Session, optional): database session. Defaults to Depends(get_db).

    Returns:
        dict: containing the movie_id and the updated click count
    """
    record = db.query(ClickStats).filter(ClickStats.movie_id == movie_id).first()
    if not record:
        record = ClickStats(movie_id=movie_id, 
                            title = db.query(Movie).filter(Movie.movie_id == movie_id).first().title,
                            recommendations_shown=0, 
                            clicks=0)
        db.add(record)
    record.clicks += 1
    db.commit()
    return {"movie_id": movie_id, "clicks": record.clicks}

# Endpoint to fetch click statistics (click percentage)
@app.get("/click_stats/")
def get_click_stats(movie_id: str, db: Session = Depends(get_db)):
    """Returns the click percentage for the given movie_id.

    Args:
        movie_id (str): The movie_id to retrieve click percentage for.
        db (Session): The database session object.


    Returns:
        dict: A dictionary with the movie_id and the click percentage.
    """
    record = db.query(ClickStats).filter(ClickStats.movie_id == movie_id).first()
    if not record or record.recommendations_shown == 0:
        return {"movie_id": movie_id, "click_percentage": 0}
    percentage = (record.clicks / record.recommendations_shown) * 100
    return {"movie_id": movie_id, "click_percentage": percentage}


@app.post("/add_movie/")
def add_movie(movie_title:str, category: str, release_date: str, user_rating: float, db: Session = Depends(get_db)):
    """
    Adds a new movie to the database.

    This endpoint takes the title, category, release date, and user rating of a movie, 
    checks if the movie already exists in the database, and if not, adds it as a new entry. 
    It also creates a corresponding rating for the new movie.

    Parameters:
    - movie_title (str): The title of the movie to add.
    - category (str): The category or genre of the movie.
    - release_date (str): The release date of the movie in 'DD-Mth-YYYY' format.
    - user_rating (float): The user-provided rating for the movie.
    - db (Session): The database session used for the operation.

    Returns:
    - dict: A message indicating the result of the operation.

    Raises:
    - HTTPException: If the movie already exists in the database.
    """
    # Check if the movie already exists
    
    existing_movie = db.query(Movie).filter(Movie.title == movie_title).first()
    if existing_movie:
        raise HTTPException(status_code=400, detail="Movie already exists")

    # Create a new Movie instance
    new_movie = Movie(
        # movie_id is generated by the database
        movie_id=str(db.query(Movie).count() + 1),
        title=str.lower(movie_title),
        release_date=release_date,
        unknown= 1 if category == "unknown" else 0,
        action= 1 if category == "action" else 0,
        adventure=1 if category == "adventure" else 0,
        animation=1 if category == "animation" else 0,
        children=1 if category == "children" else 0,
        comedy=1 if category == "comedy" else 0,
        crime=1 if category == "crime" else 0,
        documentary=1 if category == "documentary" else 0,
        drama=1 if category == "drama" else 0,
        fantasy=1 if category == "fantasy" else 0,
        filmnoir=1 if category == "filmnoir" else 0,
        horror=1 if category == "horror" else 0,
        musical=1 if category == "musical" else 0,
        mystery=1 if category == "mystery" else 0,
        romance=1 if category == "romance" else 0,
        scifi=1 if category == "scifi" else 0,
        thriller=1 if category == "thriller" else 0,
        war=1 if category == "war" else 0,
        western=1 if category == "western" else 0
        )
    
    # Create a new Rating instance
    new_rating = Rating(
        user_id='999',
        movie_id=str(db.query(Movie).count() + 1),
        rating= user_rating
    )
                     

    # Add the new movie to the database
    db.add(new_movie)
    # Add the new movie to the database
    db.add(new_rating)
    db.commit()
    db.refresh(new_movie)
    db.refresh(new_rating)
    return {"message": "Movie added successfully."}