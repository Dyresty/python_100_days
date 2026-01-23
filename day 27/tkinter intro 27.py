import tkinter as tk
window = tk.Tk()
window.title("GUI Program")
window.minsize(width=600, height=450)

mylabel = tk.Label(text="This is a label", font=("Arial", 24, "bold"))
mylabel.pack()

window.mainloop()




