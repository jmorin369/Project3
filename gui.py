import os
import tkinter as tk
import hashtb as ht
import avl as tree

currdir = os.path.dirname(__file__)

# avl tree & hash table nteraction
omap = tree.AVL()
obj = ht.HashTable()

spch = [] 
for item in tree.speeches:
    spch.append(item) # TODO: make this be in order??

def parse(text):
    word = ""
    # file = open(file)
    for line in text: 
        line = line.lower()
        for char in line: 
            if char == " " or char == "\"" or char == "," or char == "." or char == "?" or char == "…" \
                or char == "€" or char == "¦" or char >= "Ç":
                if word != "":
                    # TODO: time these functions
                    omap.add(word)
                    obj.insert(word)
                word = ""
            else:
                word += char


def makeFile(rallyList):
    text = ''
    for it in range(len(rallyList)):
        file = rallyList[it] + '.txt'
        with open(file) as f:
            text += f.read()
            # print(file)
    return text


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

def printInfo(word):
    rallyList = []
    rallyStr = ''
    selectedRallies = box.curselection()
    for i in range(len(selectedRallies)):
        rallyList.append(box.get(selectedRallies[i]))
        rallyStr += box.get(selectedRallies[i]) + '\n'
    # rallyList is a list of selected rally/file names to send to parsing function
    # TODO: call makeFile(rallyList), which will call parse(newfile) to collect appropriate data
    #       there should also be a way to retrieve the time it took to make & search each data structure
    #       this time must outputted into the info string below
    #           TODO: actually maybe move this to a different button
    parse( makeFile(rallyList) )
    # TODO: call count(word) to retrieve count and pass it to the string below
    infostr = 'You searched for: %s \n' % (word)
    infostr += 'From Rallies: \n%s' % (rallyStr)
    cntHash = obj.getCount(word)
    cntTree = 'AVL search function???'
    infostr += 'Results from:\n'
    infostr += 'Hash Table: \t\t\t AVL Tree:\n'
    infostr += 'Count: %d \t\t\t //TODO: %s' % (cntHash, cntTree)
    infostr += '//TODO: Print Search & Insert Time'
    infoLabel['text'] = infostr

# rally selection
select = tk.Frame(root, bg="black")
select.place(relx=0.05, rely=0.2, relwidth=0.2, relheight=0.7)

box = tk.Listbox(select, bg="white", selectmode=tk.BROWSE)
for x in range(len(spch)):
    box.insert(x, spch[x])
box.place(relx=0, rely=0, relwidth=1, relheight=1)
# TODO: make parse button to press upon selection
#       instruct user to parse first, then search
# TODO LAST: make sure multiple selection works?


# display info
infoFrame = tk.Frame(root, bg="black")
infoFrame.place(relx=0.30, rely=0.05, relwidth=0.6, relheight=0.3)

infoLabel = tk.Label(infoFrame, text="display info about word")
infoLabel.place(relwidth=1, relheight=1)

root.mainloop()