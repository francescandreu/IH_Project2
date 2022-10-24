import pandas as pd
import os
from os.path import exists


# Prepare a list of strings with the names of the desired playlists
def prepareWantedLists():
    list_playlists = []
    for year in range(1970, 2022):
        playlist = "Top Hits of "+str(year)
        list_playlists.append([playlist, year])
    return list_playlists

def readPlaylistsCSV():
    df = pd.read_csv('data\playlistsYearURI.csv', index_col=False)
    df.reset_index(drop=True, inplace=True)
    return df

def readTracksCSV():
    df = pd.read_csv('data\listTracks.csv', index_col=False)
    df.reset_index(drop=True, inplace=True)
    return df

def readWordCountCSV():
    df = pd.read_csv('data\wordCount.csv')
    return df

def checkFileExists(file_name):
    return exists(file_name)