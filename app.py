from http.client import responses

import streamlit as st
import pickle # to get data from .pkl file
import pandas as pd
import requests # used for API hitting

# fetch poster
def fetch_poster(movie_id):
    #this below code is not working I think it's because syntax used in below line,
    # there "format()" is giving this error -> AttributeError: 'Response' object has no attribute 'format'
    # now I get it why I got that error because I'm writing ".format()" outside the "get()" function but it must be written inside the "grt()".
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=0441e525f671d6094e04ed318f489f21&language=en-US'.format(movie_id))
    data = response.json()
    full_poster_path =  "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    return full_poster_path

    # above and below code is same
    # url = "https://api.themoviedb.org/3/movie/{}?api_key=0441e525f671d6094e04ed318f489f21&language=en-US".format(movie_id)
    # data = requests.get(url)
    # data = data.json()
    # poster_path = data['poster_path']
    # full_poster_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    # return full_poster_path


# main function : gives five movie name when we give any movie name
def recommend(movie):
    # fetching movies index
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].id

        recommended_movies.append(movies.iloc[i[0]].title)
        # fetching poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies,recommended_movies_posters


# comment below code because accessing dataset causing some problem
# #getting data from movie-recommendation-system through movies.pkl file
# movies_list = pickle.load(open('movies.pkl','rb'))

# therefore we are getting data from dictionary: movie_dict.pkl
#getting data from movie-recommendation-system through movie_dict.pkl file
movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict) # creating dataset of movies

similarity = pickle.load(open('similarity.pkl','rb'))

# main title
st.title('Movie Recommender System')

# dropdown select menu
selected_movie_name = st.selectbox(
    "Select A Movie: ",
    movies['title'].values
)

# button for movie recommendation
if st.button("Recommend"):
    names,posters = recommend(selected_movie_name) # main function

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