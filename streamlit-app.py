# imports
import streamlit as st
import requests
from myapp import recommender


# Base URL for your FastAPI server
API_URL = "http://127.0.0.1:8000"
# API_URL = "http://backend:8000" #when using docker

st.title("Movie Recommender")

# Input for movie name and transform to lowercase
movie_input = st.selectbox(label="Select a Movie", index=None,
                           options=recommender.get_movies_list(),
                           help="Select a movie to get recommendations") 

if movie_input:
    movie_input = movie_input.lower()

# If user clicks "Get Recommendations"
if st.button("Get Recommendations"):
    # And movie name is not empty
    if movie_input:
        # Call the /recommend/ endpoint
        response = requests.get(f"{API_URL}/recommend/", params={"movie": movie_input})
        
        # If the response is successful
        if response.status_code == 200:
            # Get the JSON response
            data = response.json()
            
            # Display the movie and recommendations. If recs not found, return empty list
            recs = data.get("recommendations", [])
            
            # Write recommendations. For each recommendation, display title and movie_id
            st.write("### Recommendations:")

            # Enumerate to get recommendation number, movie ID, and title
            hashmap = {n:{"movie_id": rec["movie_id"], "title": rec["title"]} for n, rec in enumerate(recs, start=1)}
            
            # Create columns
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                # Choose a recommended movie
                st.write(str.capitalize(hashmap[1]["title"]))
                # Button to register a click for the recommendation
                def click_response(): 
                    click_response = requests.post(f"{API_URL}/click/", params={"movie_id": hashmap[1]["movie_id"]})
                    if click_response.status_code == 200:
                        st.success(f"Registered click for {hashmap[1]['title']}")
                # If clicked, add a click to counter
                if st.button(label=hashmap[1]["movie_id"], on_click=click_response):
                    pass

                # Click percentage
                # Fetch and display the click percentage
                stats_response = requests.get(f"{API_URL}/click_stats/", params={"movie_id": hashmap[1]["movie_id"]})
                if stats_response.status_code == 200:
                    stats = stats_response.json()
                    click_percentage = stats.get("click_percentage", 0)
                    st.write(f"Click Rate: {click_percentage:.1f}%")

            
            with col2:
                #Choose movie 2
                st.write(str.capitalize(hashmap[2]["title"]))
                # Button to register a click for the recommendation
                def click_response(): 
                    click_response = requests.post(f"{API_URL}/click/", params={"movie_id": hashmap[2]["movie_id"]})
                    if click_response.status_code == 200:
                        st.success(f"Registered click for {hashmap[2]['title']}")
                # If clicked, add a click to counter
                if st.button(label=hashmap[2]["movie_id"], on_click=click_response):
                    pass

                # Click percentage
                # Fetch and display the click percentage
                stats_response = requests.get(f"{API_URL}/click_stats/", params={"movie_id": hashmap[2]["movie_id"]})
                if stats_response.status_code == 200:
                    stats = stats_response.json()
                    click_percentage = stats.get("click_percentage", 0)
                    st.write(f"Click Rate: {click_percentage:.1f}%")


                
            with col3:
                # 3
                st.write(str.capitalize(hashmap[3]["title"]))
                # Button to register a click for the recommendation
                def click_response(): 
                    click_response = requests.post(f"{API_URL}/click/", params={"movie_id": hashmap[3]["movie_id"]})
                    if click_response.status_code == 200:
                        st.success(f"Registered click for {hashmap[3]['title']}")
                # If clicked, add a click to counter
                if st.button(label=hashmap[3]["movie_id"], on_click=click_response):
                    pass
                
                # Click percentage
                # Fetch and display the click percentage
                stats_response = requests.get(f"{API_URL}/click_stats/", params={"movie_id": hashmap[3]["movie_id"]})
                if stats_response.status_code == 200:
                    stats = stats_response.json()
                    click_percentage = stats.get("click_percentage", 0)
                    st.write(f"Click Rate: {click_percentage:.1f}%")

            with col4:
                #4
                st.write(str.capitalize(hashmap[4]["title"]))
                # Button to register a click for the recommendation
                def click_response(): 
                    click_response = requests.post(f"{API_URL}/click/", params={"movie_id": hashmap[4]["movie_id"]})
                    if click_response.status_code == 200:
                        st.success(f"Registered click for {hashmap[4]['title']}")
                # If clicked, add a click to counter
                if st.button(label=hashmap[4]["movie_id"], on_click=click_response):
                    pass

                # Click percentage
                # Fetch and display the click percentage
                stats_response = requests.get(f"{API_URL}/click_stats/", params={"movie_id": hashmap[4]["movie_id"]})
                if stats_response.status_code == 200:
                    stats = stats_response.json()
                    click_percentage = stats.get("click_percentage", 0)
                    st.write(f"Click Rate: {click_percentage:.1f}%")

                      
            
        else:
            st.error("Movie not listed. Please try again.")
    else:
        st.warning("Please enter a movie name.")

# sidepanel
with st.sidebar:
    st.title("Add a New Movie to the Database")
    
    # Input for movie name and transform to lowercase
    new_movie = st.text_input("New Movie name:")
    if new_movie:
        new_movie = str.lower(new_movie)
    new_category = st.selectbox(index=None, label="New Movie Category", help="Select the movie category",
                                  options=["Action", "Adventure", "Animation", "Children", "Comedy", "Crime", "Documentary",
                                            "Drama", "Fantasy", "Film-Noir", "Horror", "Musical", "Mystery", "Romance",
                                            "Sci-Fi", "Thriller", "War", "Western"])
    if new_category:
        new_category = str.lower(new_category)

    new_release_dt = st.text_input("Release Date DD-Mth-YYYY", value='01-Jan-2000')
    new_rating = st.number_input("Rating", min_value=1.0, max_value=5.0, value=3.0, step=0.1)
    
    # Button to add movie
    if st.button("Add Movie"):
        # Call the /add_movie/ endpoint
        response = requests.post(f"{API_URL}/add_movie/", params={"movie_title": new_movie, 'category': new_category,
                                                                  'release_date': new_release_dt, 'user_rating': new_rating})
        if response.status_code == 200:
            st.success("Movie added successfully.")
        else:    
            st.error("Failed to add movie. Please try again.")