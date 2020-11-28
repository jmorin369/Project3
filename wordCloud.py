from wordcloud import WordCloud, STOPWORDS
import os
from PIL import Image
import numpy as np

currdir = os.path.dirname(__file__)

def make_wc(txt):
    stopwords = set(STOPWORDS)
    mask = np.array(Image.open('trump3.png'))
    wc = WordCloud(stopwords=stopwords, mask=mask, background_color="white")
    wc.generate(txt)
    wc.to_file(os.path.join(currdir, 'wc.png'))

def make_from(file):
    with open(file) as f:
        text = f.read()
        
    make_wc(text)

file = input("Please enter the file name \n")
make_from(file)

# BattleCreekDec19_2019.txt