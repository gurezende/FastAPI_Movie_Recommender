# file to create schemas for the API
from pydantic import BaseModel

class MovieCreate(BaseModel):
    movie_id: int
    title: str
    release_date: str
    unknown: int
    action: int
    adventure: int
    animation: int
    children: int
    comedy: int
    crime: int
    documentary: int
    drama: int
    fantasy: int
    filmnoir: int
    horror: int
    musical: int
    mystery: int
    romance: int
    scifi: int
    thriller: int
    war: int
    western: int
