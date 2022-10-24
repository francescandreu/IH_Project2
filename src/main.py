# Program FLOW
# 1. Data gathering: (songs.py)
#   - Establish conexion with APIs: 
#       - Spotify 
#       - Lyrics: 
#           - Json with info of the song (URL to lyrics page)
#           - Web scrapping
#   - Check conexion
# 2. Data cleaning
# 3. Data structuring
# 4. Data visualization:
#   - Top genres per year
#   - Top artists per year
#   - Most used words per genres
#   - Most used words per year 
#   - Used words per genre and year (evolution)
#   - 

import requests
import os
import json
import re
import numpy as np
import pandas as pd
from pandas import json_normalize
from dotenv import load_dotenv
from collections import Counter

import songs as so
import lyrics as ly
import files as fi

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from lyricsgenius import Genius


def main():
    load_dotenv()
    sp = so.connectToSpotify()
    genius = ly.connectToGenius()
    
    if not fi.checkFileExists('data\playlistsYearURI.csv'):
        print("Creating new Playlists file...")
        so.createPlaylistsCSV(sp)
    print("Reading existing Playlists file...")
    df_playlists = fi.readPlaylistsCSV()

    if not fi.checkFileExists("data\listTracks.csv"):
        print("Retrieving songs from online Playlists...")
        df_tracks = so.getTracksFromPlaylists(sp, df_playlists)
        columns = {0: 'song', 1: 'artists', 2: 'year'}
        df_tracks = so.renameColsDf(df_tracks, columns)
        so.createTracksCSV(df_tracks)
    else:
        print("Reading songs from local existing file...")
        df_tracks = fi.readTracksCSV()
    
    for year in range(1970, 2022):
        df_tracks_year = df_tracks[df_tracks['year'] == year]
        file_path_name = 'data\wordCount'+str(year)+'.csv'
        print(file_path_name)
        if not fi.checkFileExists(file_path_name):
            df_words_count_total = pd.DataFrame()

            for index in range(df_tracks_year.shape[0]):
                row = df_tracks_year.iloc[index]                                # Get row information (song)
                try:
                    song = genius.search_song(row.song, row.artists)            # Get lyrics of given song
                    words = ly.cleanWordStructure(song.lyrics)                  # Clean lyrics and get only the words
                    new_words = ly.cleanTypeWords(words) 

                    word_counts = dict(Counter(new_words))
                    df_word_counts = pd.DataFrame.from_dict(word_counts, orient='index')
                    df_word_counts.rename(columns= {0: 'sum'}, inplace=True)
                    df_word_counts.reset_index(inplace=True)

                    df_words_count_total = pd.concat([df_words_count_total, df_word_counts]).groupby(['index']).sum().reset_index()
                    
                except Exception as e:
                    print(e)
                    continue
            print(df_words_count_total)
            ly.createWordCountCSV(df_words_count_total, year) 
        else:
            #print("Reading word count from local existing file...")
            #df_word_count_total = fi.readWordCountCSV()
            pass
    return True

if __name__ == '__main__':
    main()