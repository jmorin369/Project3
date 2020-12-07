# TODO FIX: every time selection is finalized, the text keeps getting re-added
# TODO: make plot of comparison of word frequencies??
# TODO: the plot isnt respecting the [0,100] range for some reason

import os
import time
import tkinter as tk
import hashtb as ht
import avl as tree

from wordcloud import WordCloud, STOPWORDS
from PIL import Image
import numpy as np

import matplotlib.pyplot as plt

currdir = os.path.dirname(__file__)

omap = tree.AVL()
obj = ht.HashTable()

# turns the set of txt files from avl.py into a touple for easy manipulation
spch = [] 
for item in sorted(tree.speeches):
    spch.append(item)

treeTime = 0.0
hashTime = 0.0
wordCount = 0
# print("time initialized to:%f%f"%(treeTime, hashTime))
def parse(text):
    global treeTime
    global hashTime
    global wordCount
    # tree insertion
    startTime = time.time()
    # print("time beofre tree insertion: %f" % startTime)
    word = ""
    for line in text: 
        line = line.lower()
        for char in line: 
            if (char >= 'a' and char <= 'z') or char == '/'':
                word += char
            elif char == " ":
                if word != "":
                    omap.add(word, speech)
                word = ""
    currTime = time.time()
    # print("time after: %f" % currTime)
    treeTime = currTime - startTime
    # print("difference = %f - %f = %f" % (startTime, currTime, treeTime))

    # hash table insertion
    startTime = time.time()
    word = ""
    # print("time beofre hashtb insertion: %f" % startTime)
    for line in text: 
        line = line.lower()
        for char in line: 
            if (char >= 'a' and char <= 'z') or char == '/'':
                word += char
            elif char == " ":
                if word != "":
                    omap.add(word, speech)
                word = ""
    currTime = time.time()
    # print("time after: %f" % currTime)
    hashTime = currTime - startTime
    # print("difference = %f - %f = %f" % (startTime, currTime, hashTime))



def makeFile(rallyList):
    text = ''
    for it in range(len(rallyList)):
        file = rallyList[it] + '.txt'
        # print(file)
        with open(file) as f:
            text += f.read()
    # print(text)
    return text


def makeWC(txt):
    stopwords = set(STOPWORDS)
    # mask = np.array(Image.open('trump.png'))
    wc = WordCloud(stopwords=stopwords, background_color="white")
    wc.generate(txt)
    wc.to_file(os.path.join(currdir, 'wc.png'))
    plt.figure()
    plt.imshow(wc, interpolation="bilinear")
    plt.tight_layout(pad=0)
    plt.axis("off")
    plt.show()




# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

# from matplotlib.figure import Figure 
# from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
# NavigationToolbar2Tk) 

def testplot(): 
    
    omap.getCounts()
    lists = sorted(omap.counts.items()) # sorted by key, return a list of tuples
    count, freq = zip(*lists) # unpack a list of pairs into two tuples
    plt.bar(count[0:100], freq[0:100])
    plt.ylabel('Frequency')
    plt.xlabel('Count Value')
    plt.title('Frequency of Count Values')
    plt.show()

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------




h = 786
w = 1024
root = tk.Tk()
root.title("COP3530 Project 3 by Poli Sci Gurus")
canvas = tk.Canvas(root, height=h, width=w)
canvas.pack()

# cloud
wcPic = tk.PhotoImage(file='wc.png')
trump = tk.PhotoImage(file='trumppic.png')

trumpFrame = tk.Frame(root, bg="black")
trumpFrame.place(relx=0.3, rely=0.4, relwidth=0.6, relheight=0.5)

trumpPhoto = tk.Label(trumpFrame, image=trump)
trumpPhoto.place(relx=0, rely=0, relwidth=1, relheight=1)

cloudButton = tk.Button(trumpFrame, text="Word Cloud", command=lambda: makeWC(finalTxt))
cloudButton.place(relx=0.01, rely=0.3, relwidth=0.2, relheight=0.1)

plotButton = tk.Button(trumpFrame, text="Count-Frequency Plot", command=lambda: testplot())
plotButton.place(relx=0.26, rely=0.3, relwidth=0.3, relheight=0.1)

# def showCloud():
#     # global wcPic
#     # wcPic = tk.PhotoImage(file='wc.png')
    
#     # cloudFrame = tk.Frame(root, bg="black")
#     # cloudFrame.place(relx=0.4, rely=0.6, relwidth=0.4, relheight=0.3)

#     # cloudPhoto = tk.Label(cloudFrame, image=wcPic)
#     # cloudPhoto.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.98)


# search
searchFrame = tk.Frame(root, bg="black")
searchFrame.place(relx=0.05, rely=0.775, relwidth=0.2, relheight=0.15)

searchLabel = tk.Label(searchFrame, text="Now, search for a word or list \n of words separated by spaces:")
searchLabel.place(relx=0, rely=0, relwidth=1, relheight=0.25)

searchBar = tk.Entry(searchFrame)
searchBar.place(rely=0.25, relwidth=1, relheight=0.5)

searchButton = tk.Button(searchFrame, text="Search", command=lambda: printInfo(searchBar.get()))
searchButton.place(relx=0, rely=0.75, relwidth=1, relheight=0.25)

rallyStr, finalTxt = '', ''
def build():
    rallyList = []
    selectedRallies = box.curselection()
    for i in range(len(selectedRallies)):
        rallyList.append(box.get(selectedRallies[i]))
        global rallyStr
        rallyStr += box.get(selectedRallies[i]) + ' '
    # rallyList is a list of selected rally/file names to send to parsing function
    # makeFile(rallyList) will return a final text file with all the selected texts
    global finalTxt
    finalTxt = makeFile(rallyList)
    parse(finalTxt)

def parseSearch(words):
    wordList = []
    newstr = ''
    for i in range(0, len(words)):
        if words[i] != ' ':
            newstr += words[i]
        else:
            wordList.append(newstr)
            newstr = ''
    return wordList

def printInfo(words):
    wordList = parseSearch(words)
    cntHash, cntTree = 0, 0
    treeSrchTime, hashSrchTime = 0.0, 0.0
    infostr = 'You searched for: %s \n' % (words)
    infostr += 'From Rallies: %s\n' % (rallyStr)
    infostr += 'Total Number of Words: %d' % (wordCount)
    infoLabel1['text'] = infostr

    startTime = time.time()
    cntHash = obj.getCount(wordList[0])
    currTime = time.time()
    treeSrchTime = currTime - startTime

    startTime = time.time()
    cntTree = (omap.search(wordList[0])).count
    currTime = time.time()
    treeSrchTime = currTime - startTime

    infostr = "AVL Tree:\n\nWord Count: %d\nInsertion Time: %f\nSearch Time: %f" % (cntTree, treeTime, treeSrchTime)
    infoLabel2['text'] = infostr
    infostr = "Hash Table:\n\nWord Count: %d\nInsertion Time: %f\nSearch Time: %f" % (cntHash, hashTime, hashSrchTime)
    infoLabel3['text'] = infostr
    

# rally selection
selectFrame = tk.Frame(root, bg="black")
selectFrame.place(relx=0.05, rely=0.05, relwidth=0.2, relheight=0.7)

selectLabel = tk.Label(selectFrame, text="First, select the desired rallies: ")
selectLabel.place(relx=0, rely=0, relwidth=1, relheight=0.05)

box = tk.Listbox(selectFrame, bg="white", selectmode=tk.MULTIPLE)
for x in range(len(spch)+2):
    if (x==0):
        box.insert(len(spch)+1, "testtxt1")
    elif (x==1):
        box.insert(len(spch)+2, "testtxt2")
    else:
        box.insert(x, spch[x-2])

box.place(relx=0, rely=0.05, relwidth=1, relheight=0.9)

selectButton = tk.Button(selectFrame, text="Finalize Selection", command=lambda: build())
selectButton.place(relx=0, rely=0.95, relwidth=1, relheight=0.05)


# display info
infoFrame1 = tk.Frame(root, bg="black")
infoFrame1.place(relx=0.30, rely=0.05, relwidth=0.6, relheight=0.1)

infoFrame2 = tk.Frame(root)
infoFrame2.place(relx=0.30, rely=0.15, relwidth=0.3, relheight=0.225)

infoFrame3 = tk.Frame(root)
infoFrame3.place(relx=0.60, rely=0.15, relwidth=0.3, relheight=0.225)

newstr = ("Welcome. This program allows you to search for words said by President Trump during his rallies.\n" +
        "You can see their frequencies, compare them to each other, and more! " +
        "Follow the instructions \nto the left, and click the buttons below to " +
        "display the information as you wish.")
infoLabel1 = tk.Label(infoFrame1, text=newstr)
infoLabel1.place(relx=0, rely=0, relwidth=1, relheight=1)

newstr = ("Here, we will also be comparing\nthe performance of two different\n data structures: " +
        "An AVL Tree (left),\nand a Hash Table (right)")
infoLabel2 = tk.Label(infoFrame2, text=newstr)
infoLabel2.place(relx=0, rely=0, relwidth=1, relheight=1)

newstr = ("If you searched for more than one word,\nthe information displayed will be about\nthe first word only. " +
        "However, below you can \naccess plots that compare the frequencies\nof all of the words you entered")
infoLabel3 = tk.Label(infoFrame3, text=newstr)
infoLabel3.place(relx=0, rely=0, relwidth=1, relheight=1)

root.mainloop()