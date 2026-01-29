from pathlib import Path

import random
import string

from tkinter import *
from tkinter import messagebox


SCRIPT_DIR = Path(__file__).parent

import pandas as pd
try:
    dict = pd.read_csv(str(SCRIPT_DIR / "German words to learn.csv"))
except:
    dict = pd.read_csv(str(SCRIPT_DIR / "German 1000 words.csv"))
print(dict)

# Get the directory where this script is located


BACKGROUND_COLOR = "#B1DDC6"

current_index = 0
after_id = None

def button_clicked(correct):
    global current_index, after_id, dict
    if correct == 1:
        dict = dict.drop(current_index).reset_index(drop=True)
    if after_id is not None:
        window.after_cancel(after_id)
    current_index = random.randint(0, len(dict)-1)
    random_word = dict.iloc[current_index, 0]
    canvas.itemconfig(card_image, image=cardfrontimage)
    canvas.itemconfig(canvas_word, text = random_word, fill = "black")
    canvas.itemconfig(canvas_lang, text = "German", fill = "black")
    canvas.tag_raise(canvas_word)
    canvas.tag_raise(canvas_lang)
    after_id = window.after(3000, func=flip_card)


def flip_card():
    global current_index
    canvas.itemconfig(card_image, image=cardbackimage)
    english_word = dict.iloc[current_index, 1]
    canvas.itemconfig(canvas_lang, text = "English", fill = "white")
    canvas.itemconfig(canvas_word, text = english_word, fill = 'white')
    canvas.tag_raise(canvas_word)
    canvas.tag_raise(canvas_lang)

def save():
    global dict
    data_write = pd.DataFrame(dict)
    data_write.to_csv(str(SCRIPT_DIR / "German words to learn.csv"), index=False)
    messagebox.showinfo(title="Saved", message=f"The words to learn have been saved! You can close or continue with the learning")

window = Tk()
window.title("German words Flashcards")
window.config(padx=50, pady=50, bg= BACKGROUND_COLOR)

canvas = Canvas(width=800, height=526, highlightthickness=0, background=BACKGROUND_COLOR)
cardbackimage = PhotoImage(file=str(SCRIPT_DIR / "card_back.png"))
cardfrontimage = PhotoImage(file=str(SCRIPT_DIR / "card_front.png"))
card_image = canvas.create_image(400, 263, image=cardfrontimage)  
canvas.grid(column=0, row=0,  columnspan=2)
canvas_lang = canvas.create_text(400, 150, text="German", font=("Ariel", 40, "italic"))
current_index = random.randint(0, len(dict)-1)
random_word = dict.iloc[current_index, 0]
canvas_word = canvas.create_text(400, 263, text=random_word, font=("Ariel", 60, "bold"))
after_id = window.after(3000, func=flip_card)


crossmarkimage = PhotoImage(file=str(SCRIPT_DIR / "wrong.png"))
button2 = Button(image=crossmarkimage, highlightthickness=0, command=lambda: button_clicked(0))
button2.grid(column=0, row=1)

checkmarkimage = PhotoImage(file=str(SCRIPT_DIR / "right.png"))
button1 = Button(image=checkmarkimage, highlightthickness=0, command =lambda: button_clicked(1))
button1.grid(column=1, row=1)

button3 = Button(width= 15, height= 2, text="Save", highlightthickness=0, command = save)
button3.grid(column=0, row=2, columnspan=2)

window.mainloop()

