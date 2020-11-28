import tkinter as tk

h = 600
w = 800

root = tk.Tk()

canvas = tk.Canvas(root, height=h, width=w)
canvas.pack()

# frame = tk.Frame(root)
# frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

# background_image = tk.PhotoImage(file='trump3.png')
# background_label = tk.Label(frame, image=background_image)
# background_label.place(relwidth=1, relheight=1)

# label = tk.Label(frame, bg="gray", text="Select Rallies")
# label.place(relx=0.1, rely=0.1, relwidth=0.2, relheight=0.1)

search = tk.Frame(root, bg="black")
search.place(relx=0.05, rely=0.05, relwidth=0.2, relheight=0.1)

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


info = tk.Frame(root, bg="black")
info.place(relx=0.30, rely=0.05, relwidth=0.6, relheight=0.3)

cloud = tk.Frame(root, bg="black")
cloud.place(relx=0.30, rely=0.4, relwidth=0.6, relheight=0.5)

root.mainloop()