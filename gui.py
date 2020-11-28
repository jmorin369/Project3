import tkinter as tk

h = 600
w = 800

root = tk.Tk()
canvas = tk.Canvas(root, height=h, width=w)
canvas.pack()


# cloud
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
    tempstr = ''
    selectedRallies = box.curselection()
    for i in range(len(selectedRallies)):
        tempstr += str(selectedRallies[i]) + ', '
    tempstr = 'From rallies ' + tempstr
    infostr = 'You searched for: %s \n%s\n%s was said x times \n' % (word, tempstr, word)
    linfo['text'] = infostr

# rally selection
select = tk.Frame(root, bg="black")
select.place(relx=0.05, rely=0.2, relwidth=0.2, relheight=0.7)

box = tk.Listbox(select, bg="white", selectmode=tk.EXTENDED)
for x in range(31):
    if x==0:
        box.insert(x, "ALL")
    else:
        box.insert(x, str(x))
box.place(relx=0, rely=0, relwidth=1, relheight=1)
# call function with appropriate file names


# display info
info = tk.Frame(root, bg="black")
info.place(relx=0.30, rely=0.05, relwidth=0.6, relheight=0.3)

linfo = tk.Label(info, text="display info about word")
linfo.place(relwidth=1, relheight=1)

root.mainloop()