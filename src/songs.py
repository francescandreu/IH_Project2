# 1 Goal:
# Get Playlists for Top hits from 1970 until 2021
# Get songs in this playlists
# Add them all together into a PD with new column being YEAR
# Save the into a .CSV

import os
from os.path import exists
import pandas as pd
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import files as fi


# --------------------- SPOTIFY ---------------------
def connectToSpotify():
    cid = os.getenv('SPOTIFY_CLIENT_ID')
    secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    try:
        client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
        sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
        return sp
    except Exception as e:
        print(e)
    return False


# --------------------- PLAYLISTS --------------------- 
def searchPlaylists(sp, list_of_playlists):
    new_list = []
    for name, year in list_of_playlists:
        results = sp.search(q=name, limit=1, type='playlist')
        items = results['playlists']['items']
        if len(items) > 0:
            playlist = items[0]
            new_list.append([playlist['name'], playlist['uri'], year])
    return new_list


def createPlaylistsCSV(sp):
    lp = fi.prepareWantedLists()
    lp_year_uri = searchPlaylists(sp, lp)
    df = pd.DataFrame(lp_year_uri)
    df.columns=['name', 'uri', 'year']    
    df.to_csv('data/playlistsYearURI.csv', index=False)
    return True


def getTracksInPlaylist(sp, uri, year):
    list_of_songs = []
    tracks = sp.playlist_tracks(uri)["items"]
    for track in tracks:
        track_name = track["track"]["name"]   #Track name
        track_name = track_name.split('-')[0].strip().lower()
        artist_name = track["track"]["artists"][0]["name"]  #Main Artist
        list_of_songs.append([track_name, artist_name.lower(), year])
    return list_of_songs


# --------------------- TRACKS --------------------- 
def createTracksCSV(df):
    df.to_csv('data/listTracks.csv', index=False)
    return True


def getTracksFromPlaylists(sp, df):
    df2 = pd.DataFrame()
    for index in range(df.shape[0]):   # Loop all the playlists
        actualYear = df.iloc[index].year
        tracks_in_playlist = getTracksInPlaylist(sp, df.iloc[index].uri, actualYear)
        for track in tracks_in_playlist:
            s1 = pd.Series(track)
            df2 = pd.concat([df2, s1.to_frame().T], ignore_index=True)
        print(f"Year {actualYear} completely added.")
    os.system("clear")
    return df2


def renameColsDf(df, col):
    df.rename(columns=col, inplace=True, errors='raise')
    return df