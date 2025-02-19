# Movie Recommender

This project is a movie recommender system built with FastAPI, SQLite (*or PostgreSQL*), and Streamlit. <br>
It uses the MovieLens 100k dataset to generate movie recommendations based on user ratings. In addition, the app tracks how many times each recommendation is clicked. You can also add new movies via an API endpoint.

## Table of Contents

- [Dataset](#dataset)
- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Getting Started](#getting-started)
  - [Running Locally (Without Docker)](#running-locally-without-docker)
  - [Running with Docker & Docker Compose](#running-with-docker--docker-compose)
- [API Endpoints](#api-endpoints)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)


## Dataset
You can find the dataset in this link [https://grouplens.org/datasets/movielens/100k/](https://grouplens.org/datasets/movielens/100k/).
Find out more in the Readme file in the \data\ folder.

## Features

- **Movie Recommendation Engine:** Generate recommendations using cosine similarity.
- **Click Tracking:** Monitor how many times recommendations are clicked.
- **Backend API:** FastAPI provides endpoints for recommendations, click tracking, and adding new movies.
- **Frontend:** A Streamlit app that allows users to enter a movie name, view recommendations, and register clicks.
- **Dockerized Deployment:** Both FastAPI and Streamlit are containerized using Docker and orchestrated with Docker Compose.

## Project Structure

movie-recommender/ 
├── backend/ # FastAPI backend 
│ ├── myapp/ # FastAPI application package 
│ │ ├── init.py 
│ │ ├── main.py # FastAPI app 
│ │ ├── database.py # Database connection and session setup 
│ │ ├── models.py # SQLAlchemy models 
│ │ ├── recommender.py # Recommendation engine 
│ │ └── schemas.py # Pydantic schemas for validation  
│ ├── sql_load.py # Script to create/load database tables and initial data 
│ ├── requirements.txt # Python dependencies for backend 
│ └── Dockerfile.backend # Dockerfile for FastAPI backend 
├── streamlit_app.py # Streamlit application 
├── requirements.txt # Python dependencies for Streamlit app 
└── Dockerfile # Dockerfile for Streamlit app 
├── docker-compose.yml # Docker Compose file to run both backend and frontend 
└


## Requirements

- Docker & Docker Compose
- Python 3.12 if running locally without Docker
`fastapi` >= 0.115.8
`numpy` >= 2.2.3
`pandas` >= 2.2.3
`psycopg2-binary` >= 2.9.10
`scikit-learn` >= 1.6.1
`sqlalchemy` >= 2.0.38
`streamlit` >= 1.42.1
`uvicorn` >= 0.34.0

## Getting Started

### Running Locally (Without Docker)

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/gurezende/FastAPI_Movie_Recommender.git
   cd movie-recommender
   ```

2. **Backend Setup:**

Create a virtual environment and install dependencies:
```bash
python -m venv env
source env/bin/activate    # On Windows: .\env\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

3. **Run FastAPI**
```bash
uvicorn app.main:app --reload
```


