# 2 Goal:
# Given a df with the list of all the songs wanted:
# Connect to LYRICS API and download the lyrics for all the songs
# Count each word for all songs
# Save counts by song/genre/year into .CSV

import re
import os
from dotenv import load_dotenv
from lyricsgenius import Genius

def connectToGenius():
    url = "https://www.stands4.com/services/v2/lyrics.php"
    token = os.getenv('LYRICS_CLIENT_ID')
    try:
        genius = Genius(token)
        return genius
    except Exception as e:
        print(e)
    return False

def cleanTypeWords(words):
    new_words = []
    pronouns = ['i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them']
    determiners = ['the', 'a', 'an', 'this', 'that', 'these', 'those', 'my', 'your', 'his', 'her', 'its', 'our', 'their']
    conjunctions = ['and', 'but', 'for', 'nor', 'or', 'so', 'yet']
    flex = ['ive', 'im', 'youre', 'youve']
    prepositions = ['above', 'across', 'against', 'along', 'among', 'around', 'at', 'before', 'behind', 'below', 'beneath', 
                    'beside', 'between', 'by', 'down', 'from', 'in', 'into', 'near', 'of', 'off', 'on', 'to', 'toward', 
                    'under', 'upon', 'with', 'within']
    for word in words:
        if (word.lower() not in pronouns) and (word.lower() not in determiners) and (word.lower() not in flex) and (word.lower() not in conjunctions) and(word.lower() not in prepositions):
            new_words.append(word.lower())
    return new_words


def createWordCountCSV(df, year):
    file_name = 'data/wordCount'+str(year)+'.csv'
    df.to_csv(file_name, index=False)
    return True

def cleanWordStructure(lyrics):
    lyrics_wk = re.sub("(\[[^][]*])", "", lyrics)  # Remove all words inside []
    lyrics_wk = lyrics_wk.replace("'", "")              # Join abreviated words
    words = re.findall(r'\w+', lyrics_wk)
    words = [word.lower() for word in words]
    words[-1] = re.findall('(\D+)', words[-1])[0]
    index = words.index('lyrics')
    words = words[index+1:]
    return words