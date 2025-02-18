# imports
import streamlit as st
import requests

# Base URL for your FastAPI server
API_URL = "http://127.0.0.1:8000"

st.title("Movie Recommender")

# Input for movie name and transform to lowercase
movie_input = st.text_input("Enter a movie name:") 
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
            for rec in recs:
                movie_id = rec.get("movie_id")
                title = rec.get("title")
                
                # Create a Streamlit columns
                col1, col2, col3 = st.columns([3, 1, 2])

                # Col 1 is for the movie title
                with col1:
                    st.write(title)

                # Col 2 is for the click button to select the recommendation
                with col2:
                    # Button to register a click for the recommendation
                    if st.button(label="Click", key=str(movie_id)):

                        # If button is clicked, call the /click/ endpoint
                        click_response = requests.post(f"{API_URL}/click/", params={"movie_id": movie_id})
                        if click_response.status_code == 200:
                            st.success(f"Registered click for {title}")
                
                # Col 3 is for the click percentage
                with col3:
                    # Fetch and display the click percentage
                    stats_response = requests.get(f"{API_URL}/click_stats/", params={"movie_id": movie_id})
                    if stats_response.status_code == 200:
                        stats = stats_response.json()
                        click_percentage = stats.get("click_percentage", 0)
                        st.write(f"Click Rate: {click_percentage:.1f}%")
        else:
            st.error("Movie not listed. Please try again.")
    else:
        st.warning("Please enter a movie name.")
