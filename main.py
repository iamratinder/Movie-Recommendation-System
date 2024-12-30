import streamlit as st
import pickle 
import pandas as pd
import pathlib
import requests



def loadCSS(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

css_path = pathlib.Path('styles.css')
loadCSS(css_path)

api_key = st.secrets["api_keys"]["my_api_key"]
def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US')
    data = response.json()
    return "http://image.tmdb.org/t/p/w500" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]

    recommended_movies = []
    recommended_movie_posters = []  
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from API
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movie_posters

import gzip

# Input file (compressed file) and output (optional, for uncompressed storage)
compressed_file = 'compressed_movie_dict.pkl.gz'

# Open the compressed file and load its contents
with gzip.open(compressed_file, 'rb') as f:
    movies_dict = pickle.load(f)

    
compressed_file2 = 'compressed_similarity.pkl.gz'

# Open the compressed file and load its contents
with gzip.open(compressed_file2, 'rb') as f:
    similarity = pickle.load(f)


# movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
# similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommendation System')

selected_movie_name = st.selectbox(
    "Enter a Movie : ",
    movies['title'].values,
    index=None,
    placeholder="Select a Movie...",
    key='selectbox'
)


if st.button("Recommend", use_container_width=True, key="green"):
    if selected_movie_name:
        names,posters = recommend(selected_movie_name)
        col1, col2, col3, col4 = st.columns(4)
        col5, col6, col7, col8 = st.columns(4)
        st.subheader("Recommendations :")
        col9, col10, col11, col12 = st.columns(4)

        for i in range(0,9,3):
            col1, col2, col3, col4, col5 = st.columns([2,0.5,2,0.5,2])
            with col1:
                st.image(posters[i])
                st.text(names[i])
            with col3:
                st.image(posters[i+1])
                st.text(names[i+1])
            with col5:
                st.image(posters[i+2])
                st.text(names[i+2])
            
            col1 = st.columns(1)
        
        col1, col2, col3, col4, col5 = st.columns([2,0.5,2,0.5,2])
        with col1:
                st.image(posters[9])
                st.text(names[9])

        col1, col2, col3 = st.columns([1, 1, 1])
        with col3:
            st.button("Clear Recommendations")
    else:
        st.warning("Please select a movie before proceeding!")
        
else:
    st.write("")

