import tkinter as tk
window = tk.Tk()
window.title("GUI Program")
window.minsize(width=600, height=450)
window.config(padx=50, pady=50)

mylabel = tk.Label(text="This is a label", font=("Arial", 24, "bold"))
mylabel.grid(column=0, row=0)
mylabel.config(padx=20, pady=20)

# Button
def button_clicked():
    mylabel.config(text="New Text")
button = tk.Button(text="Click Me", command=button_clicked)
button.grid(column=1, row=1)
button.config(padx=5, pady=5)

#Button 
def button2_clicked():
    mylabel.config(text=input.get())
button2 = tk.Button(text="Update Text", command=button2_clicked)
button2.grid(column=2, row=0)
button2.config(padx=5, pady=5)

# Entry
input = tk.Entry(width=10)
print(input.get())
input.grid(column=3, row=2)

window.mainloop()


#Pack - Pack widgets next to each other, top to bottom. 
#Can specify side=LEFT, RIGHT, TOP, BOTTOM

#Place - Place widgets at an exact location you specify.
#Use x and y coordinates.
#Not responsive to window resizing.

#Grid - Place widgets in a 2D grid.
#Specify row and column.
#More flexible than pack.

#Cannot mix grid and pack in the same window.


#Padding - space around widgets
#padx and pady for x and y padding