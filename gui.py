import os
import time
import avl as tree
import hashtb as ht
import tkinter as tk
from pathlib import Path

import numpy as np
from PIL import Image
from wordcloud import WordCloud, STOPWORDS

import matplotlib
import matplotlib.pyplot as plt

currdir = os.path.dirname(__file__)
omap = tree.AVL()
obj = ht.HashTable()
# turns the set of txt files from avl.py into a touple for easy manipulation
spch = [] 
for item in sorted(tree.speeches):
    spch.append(item)


wordCount = 0
treeTime, hashTime = 0.0, 0.0
def parse(text):
    global treeTime
    global hashTime
    global wordCount
    wordCount = 0
    treeTime, hashTime = 0.0, 0.0
    
    # tree parsing and insertion
    startTime = time.time()
    word = ""
    for line in text: 
        line = line.lower()
        for char in line: 
            if (char >= 'a' and char <= 'z') or char == '\'':
                word += char
            elif char == " ":
                if word != "":
                    omap.add(word)
                    wordCount += 1
                word = ""
    currTime = time.time()
    treeTime = currTime - startTime

    # hash table parsing and insertion
    startTime = time.time()
    word = ""
    for line in text: 
        line = line.lower()
        for char in line: 
            if (char >= 'a' and char <= 'z') or char == '\'':
                word += char
            elif char == " ":
                if word != "":
                    obj.insert(word)
                word = ""
    currTime = time.time()
    hashTime = currTime - startTime


def makeFile(rallyList):
    text = ''
    for it in range(len(rallyList)):
        full_path =  currdir + "/Speeches/"
        full_path += rallyList[it] + '.txt'
        print(full_path)
        with open(full_path) as f:
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


def freqPlot(): 
    startTime = time.time()
    obj.getCounts()
    currTime = time.time()
    hashCtTime = currTime - startTime

    startTime = time.time()
    omap.getCounts()
    currTime = time.time()
    treeCtTime = currTime - startTime

    infoLabel2['text'] += '\nTraversal Time: %f' % (hashCtTime)
    infoLabel3['text'] += '\nTraversal Time: %f' % (treeCtTime)
    
    pairs = sorted(omap.counts.items())
    count, freq = zip(*pairs)
    plt.bar(count[0:50], freq[0:50])
    plt.ylabel('Frequency')
    plt.xlabel('Count Value')
    plt.title('Frequency of Count Values')
    plt.show()


def countPlot():
    global wordInfo
    global countInfo
    plt.bar(wordInfo, countInfo)
    plt.ylabel('Frequency')
    plt.title('Counts of Searched Words')
    plt.show()


def timePlot():
    global timeInfo1
    global timeInfo2
    fig, ax = plt.subplots()
    x = np.arange(len(wordInfo))
    plt.bar(x - 0.35/2, timeInfo1, color = 'b', width = 0.35, label="Hash Table")
    plt.bar(x + 0.35/2, timeInfo2, color = 'g', width = 0.35, label="AVL Tree")
    plt.ylabel('Time (s)')
    plt.title('Search Time Comparison')
    ax.set_xticks(x)
    ax.set_xticklabels(wordInfo)
    ax.legend()
    fig.tight_layout()
    plt.show()


h = 786
w = 1024
root = tk.Tk()
root.title("COP3530 Project 3 by Poli Sci Gurus")
canvas = tk.Canvas(root, height=h, width=w)
canvas.pack()


# buttons frame
wcPic = tk.PhotoImage(file='wc.png')
trump = tk.PhotoImage(file='trumppic.png')

trumpFrame = tk.Frame(root, bg="black")
trumpFrame.place(relx=0.3, rely=0.4, relwidth=0.6, relheight=0.5)

trumpPhoto = tk.Label(trumpFrame, image=trump)
trumpPhoto.place(relx=0, rely=0, relwidth=1, relheight=1)

cloudButton = tk.Button(trumpFrame, text="Word Cloud", command=lambda: makeWC(finalTxt))
cloudButton.place(relx=0.2, rely=0.32, relwidth=0.2, relheight=0.1)

plotButton = tk.Button(trumpFrame, text="Count-Frequency Plot", command=lambda: freqPlot())
plotButton.place(relx=0.15, rely=0.47, relwidth=0.3, relheight=0.1)

plotButton2 = tk.Button(trumpFrame, text="Word-Frequency Plot", command=lambda: countPlot())
plotButton2.place(relx=0.15, rely=0.62, relwidth=0.3, relheight=0.1)

plotButton3 = tk.Button(trumpFrame, text="Time Comparison Plot", command=lambda: timePlot())
plotButton3.place(relx=0.15, rely=0.77, relwidth=0.3, relheight=0.1)


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
    global rallyStr
    global finalTxt
    rallyStr, finalTxt = '', ''
    rallyList = []
    selectedRallies = box.curselection()
    for i in range(len(selectedRallies)):
        rallyList.append(box.get(selectedRallies[i]))
        # design choice: only display the first 3 selected rallies
        if i<3:
            rallyStr += box.get(selectedRallies[i]) + ' '
        elif i==4:
            rallyStr += '...'
    # rallyList is a list of selected rally/file names to send to parsing function
    # makeFile(rallyList) will return a final text file with all the selected texts
    finalTxt = makeFile(rallyList)
    parse(finalTxt)


# returns a list of the words entered into the search bar
def parseSearch(words):
    wordList = []
    newstr = ''
    for i in range(0, len(words)):
        if words[i] != ' ':
            newstr += words[i]
        else:
            wordList.append(newstr)
            newstr = ''
    wordList.append(newstr)
    newstr = ''
    return wordList


# prints info about first word's count and retrieval time
wordInfo, countInfo, timeInfo1, timeInfo2 = [], [], [], []
def printInfo(words):
    global wordInfo
    global countInfo
    global timeInfo1
    global timeInfo2
    wordInfo, countInfo, timeInfo1, timeInfo2 = [], [], [], []

    cntHash, cntTree = 0, 0
    treeSrchTime, hashSrchTime = 0.0, 0.0

    wordList = parseSearch(words)
    wordInfo = wordList
    
    infostr = 'You searched for: %s \n' % (wordList[0])
    infostr += 'From Rallies: %s\n' % (rallyStr)
    infostr += 'Total Number of Words: %d' % (wordCount)
    infoLabel1['text'] = infostr

    for x in range(len(wordList)):
        startTime = time.time()
        cntHash = obj.getCount(wordList[x])
        currTime = time.time()
        hashSrchTime = currTime - startTime
        if x==0: # first word, so store value for output
            ht = hashSrchTime 
        # vector of times for each word search with Hash table
        timeInfo1.append(hashSrchTime)

        startTime = time.time()
        cntTree = (omap.search(wordList[x])).count
        currTime = time.time()
        treeSrchTime = currTime - startTime
        if x==0: # first word, so store value for output
            tt = treeSrchTime
        # vector of times for each word searched with AVL tree
        timeInfo2.append(treeSrchTime)
        
        # vector of counts for each word
        countInfo.append(cntHash)

    infostr = "AVL Tree:\n\nWord Count: %d\nInsertion Time: %f\nSearch Time: %f" % (cntTree, treeTime, tt)
    infoLabel2['text'] = infostr
    infostr = "Hash Table:\n\nWord Count: %d\nInsertion Time: %f\nSearch Time: %f" % (cntHash, hashTime, ht)
    infoLabel3['text'] = infostr
    

# rally selection
selectFrame = tk.Frame(root, bg="black")
selectFrame.place(relx=0.05, rely=0.05, relwidth=0.2, relheight=0.7)

selectLabel = tk.Label(selectFrame, text="First, select the desired rallies: ")
selectLabel.place(relx=0, rely=0, relwidth=1, relheight=0.05)

box = tk.Listbox(selectFrame, bg="white", selectmode=tk.MULTIPLE)
for x in range(len(spch)):
    box.insert(x, spch[x])

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