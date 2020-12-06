import os
import time
import tkinter as tk
import hashtb as ht
import avl as tree

from wordcloud import WordCloud, STOPWORDS
from PIL import Image
import numpy as np

currdir = os.path.dirname(__file__)

omap = tree.AVL()
obj = ht.HashTable()


# turns the set of txt files from avl.py into a touple for easy manipulation
spch = [] 
for item in tree.speeches:
    spch.append(item) # TODO: make this be in order??

treeTime = 0.0
hashTime = 0.0
print("time initialized to:%f%f"%(treeTime, hashTime))
def parse(text):
    # tree insertion
    treeStart = time.time()
    print("time beofre tree insertion: %f" % treeStart)
    word = ""
    for line in text: 
        line = line.lower()
        for char in line: 
            if char == " " or char == "\"" or char == "," or char == "." or char == "?" or char == "…" \
                or char == "€" or char == "¦" or char >= "Ç":
                if word != "":
                    # TODO: time these functions
                    omap.add(word)
                word = ""
            else:
                word += char
    currTime = time.time()
    print("time after: %f" % currTime)
    global treeTime
    treeTime = currTime - treeStart
    print("difference = %f - %f = %f" % (treeStart, currTime, treeTime))

    # hash table insertion
    hashStart = time.time()
    word = ""
    print("time beofre hashtb insertion: %f" % hashStart)
    for line in text: 
        line = line.lower()
        for char in line: 
            if char == " " or char == "\"" or char == "," or char == "." or char == "?" or char == "…" \
                or char == "€" or char == "¦" or char >= "Ç":
                if word != "":
                    # TODO: time these functions
                    obj.insert(word)
                word = ""
            else:
                word += char
    currTime = time.time()
    print("time after: %f" % currTime)
    global hashTime
    hashTime = currTime - hashStart
    print("difference = %f - %f = %f" % (hashStart, currTime, hashTime))



def makeFile(rallyList):
    text = ''
    for it in range(len(rallyList)):
        file = rallyList[it] + '.txt'
        with open(file) as f:
            text += f.read()
    print(file)
    return text


def makeWC(txt):
    stopwords = set(STOPWORDS)
    mask = np.array(Image.open('trump3.png'))
    wc = WordCloud(stopwords=stopwords, mask=mask, background_color="white")
    wc.generate(txt)
    wc.to_file(os.path.join(currdir, 'wc.png'))


h = 600
w = 800
root = tk.Tk()
canvas = tk.Canvas(root, height=h, width=w)
canvas.pack()

# cloud
# TODO: make sure cloud is retrieving proper text file

wcPic = tk.PhotoImage(file='wc.png')
trump = tk.PhotoImage(file='trump3.png')

trumpFrame = tk.Frame(root, bg="black")
trumpFrame.place(relx=0.3, rely=0.4, relwidth=0.6, relheight=0.5)

trumpPhoto = tk.Label(trumpFrame, image=trump)
trumpPhoto.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.98)

cloudButton = tk.Button(trumpFrame, text="show wordcloud", command=lambda: showCloud())
cloudButton.place(relx=0.01, rely=0.01, relwidth=0.3, relheight=0.1)

def showCloud():
    cloudFrame = tk.Frame(root, bg="black")
    cloudFrame.place(relx=0.4, rely=0.6, relwidth=0.4, relheight=0.3)

    cloudPhoto = tk.Label(cloudFrame, image=wcPic)
    cloudPhoto.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.98)


# search
searchFrame = tk.Frame(root, bg="black")
searchFrame.place(relx=0.05, rely=0.05, relwidth=0.2, relheight=0.1)

searchLabel = tk.Label(searchFrame, text="enter word:")
searchLabel.place(relwidth=0.5, relheight=0.5)

searchBar = tk.Entry(searchFrame)
searchBar.place(rely=0.5, relwidth=1, relheight=0.5)

searchButton = tk.Button(searchFrame, text="search", command=lambda: printInfo(searchBar.get()))
searchButton.place(relx=0.5, relwidth=0.5, relheight=0.5)

rallyStr = ''
def build():
    rallyList = []
    selectedRallies = box.curselection()
    for i in range(len(selectedRallies)):
        rallyList.append(box.get(selectedRallies[i]))
        global rallyStr
        rallyStr += box.get(selectedRallies[i]) + '\n'
    # rallyList is a list of selected rally/file names to send to parsing function
    # makeFile(rallyList) will return a final text file with all the selected texts
    finalTxt = makeFile(rallyList)
    parse(finalTxt)
    makeWC(finalTxt)

def printInfo(word):
    cntHash = 0
    cntTree = 0
    infostr = 'You searched for: %s \n' % (word)
    infostr += 'From Rallies: \n%s' % (rallyStr)
    cntHash = obj.getCount(word)
    cntTree = (omap.search(word)).count
    infostr += 'Results from:\n'
    infostr += 'Hash Table: \t\t\t AVL Tree:\n'
    infostr += 'Count: %d \t\t\t Count: %d\n' % (cntHash, cntTree)
    infostr += 'Insertion Time: %f \t\t Insertion Time: %f' % (hashTime, treeTime)
    infoLabel['text'] = infostr

# rally selection
selectFrame = tk.Frame(root, bg="black")
selectFrame.place(relx=0.05, rely=0.2, relwidth=0.2, relheight=0.7)

box = tk.Listbox(selectFrame, bg="white", selectmode=tk.MULTIPLE)
for x in range(len(spch)+2):
    if (x==0):
        box.insert(len(spch)+1, "testtxt1")
    elif (x==1):
        box.insert(len(spch)+2, "testtxt2")
    else:
        box.insert(x, spch[x-2])

box.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)

selectButton = tk.Button(selectFrame, text="finalize selection", command=lambda: build())
selectButton.place(relx=0, rely=0, relwidth=1, relheight=0.1)


# display info
infoFrame = tk.Frame(root, bg="black")
infoFrame.place(relx=0.30, rely=0.05, relwidth=0.6, relheight=0.3)

infoLabel = tk.Label(infoFrame, text="display info about word")
infoLabel.place(relwidth=1, relheight=1)

root.mainloop()