import streamlit as st
import pickle
import numpy as np
import requests
import bz2

# Load the movies data
movies_df = pickle.load(open('movies.pkl', 'rb'))
movies_list = movies_df['title'].values

# Load the compressed similarity_part1.pkl.bz2 and similarity_part2.pkl.bz2 files
with bz2.open('similarity_part1.pkl.bz2', 'rb') as f1:
    similarity_part1 = pickle.load(f1)

with bz2.open('similarity_part2.pkl.bz2', 'rb') as f2:
    similarity_part2 = pickle.load(f2)

# Combine the two parts into one similarity matrix
similarity = np.vstack((similarity_part1, similarity_part2))

# Function to fetch the poster
def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=022f6c5066f4ce89ebf88c4a73a056dc&&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

# Function to recommend movies
def recommend(movie):
    movie_index = list(movies_list).index(movie)  # Get the index of the selected movie
    distances = similarity[movie_index]  # Get the similarity scores
    list1 = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_poster = []
    for i in list1:
        movie_id = movies_df.iloc[i[0]].movie_id
        recommended_movies.append(movies_df.iloc[i[0]].title)  # Get the movie title from the DataFrame
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster

st.title('Movie Recommender System')

# Dropdown menu for movie selection
selected_movie = st.selectbox(
    'Which movie did you watch last?',
    movies_list
)

# Button to generate recommendations
if st.button('Recommend'):
    names, posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
