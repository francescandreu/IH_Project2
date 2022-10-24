# IH_Project2

# Most used word in Top Hit songs

## Project description
This project goal is to obtain the Top100 segons from the year 1970 until 2021. From those songs, analyize the word frequency and obtaing which are the most utilitzed in the Top hit songs for every year.

## Table of contents
1. Libraries
2. How to run
3. Code structure

# 1. Libraries
The libraries needed for the execution of this project are as follows:

    - Pandas
    - Numpy
    - Dotenv (load_dotenv)
    - Collections (Counter)
    - Spotipy
    - Spotipy.oauth2 (SpotifyClientCredentials)
    - Lyricsgenius (Genius)
    - Os
    - Os.path (exists)
    - Re

For the visulization the following libraries are needed:

    - Seaborn
    - Matplotlib.pyplot
    - Nltk
    - Nltk.corpus (stopwords)
    - Wordcloud (WordCloud)

# 2. How to run
In order to execute the data gathering and processing of this project you only need to execute the main.py.

For the visualization it's only needed the viz.ipnyb

# 3. Code structure 
The project is mainly divided in three steps:
- Data gathering
- Data processing
- Data visualization

Each of these steps are crucial for the end goal of developing a pipeline to work with all the data. 

In the first step we will make use of the Spotify API and the library Spotipy to get the names and artists of all the Top songs that will be analyzed.

In order to get the lyrics for each of them, the use of the Lyricgenius API will be crucial.

To visualize the data we will make use of a Jupiter Notebook file, which allows for a easy and intuitive implementation. Various libraries will be made use of, to plot mainly using Seaborn. And Wordcloud to create a weigheted wordcloud to visualize the worked data.