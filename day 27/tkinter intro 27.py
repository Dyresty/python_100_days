import tkinter as tk
window = tk.Tk()
window.title("GUI Program")
window.minsize(width=600, height=450)

mylabel = tk.Label(text="This is a label", font=("Arial", 24, "bold"))
#mylabel["text"] = "New Text"
#mylabel.config(text="New Text")
mylabel.pack()

mylabel.config(text="New Text")



# Button
def button_clicked():
    mylabel.config(text=input.get())

button = tk.Button(text="Click Me", command=button_clicked)
button.pack()



# Entry
input = tk.Entry(width=30)
input.pack()
print(input.get())



# Text    
text = tk.Text(height=5, width=30)
#focus puts cursor into text box
text.focus()
text.insert(tk.END, "Example of multi-line text entry.")
print(text.get("1.0", tk.END))
text.pack()



# Spinbox
def spinbox_used():
    print(spinbox.get())
spinbox = tk.Spinbox(from_=0, to=10, width=5, command=spinbox_used)
spinbox.pack()



# Scale
def scale_used(value):
    print(value)
scale = tk.Scale(from_=0, to=100, command=scale_used)
scale.pack()

# Checkbutton
def checkbutton_used():
    print(checked_state.get())
checked_state = tk.IntVar()
checkbutton = tk.Checkbutton(text="Is On?", variable=checked_state, command=checkbutton_used)
checkbutton.pack()


def radio_used():
    print(radio_state.get())  
radio_state = tk.IntVar()
radiobutton1 = tk.Radiobutton(text="Option 1", value=1, variable=radio_state, command=radio_used)
radiobutton2 = tk.Radiobutton(text="Option 2", value=2, variable=radio_state, command=radio_used)
tk.command=radio_used
radiobutton1.pack()
radiobutton2.pack()


# Listbox
listbox = tk.Listbox(height=4)
fruits = ["Apple", "Banana", "Cherry", "Date"]
for item in fruits:
    listbox.insert(fruits.index(item), item)
def listbox_used(event):
    print(listbox.get(listbox.curselection()))  
listbox.bind("<<ListboxSelect>>", listbox_used)
listbox.pack()

window.mainloop()

