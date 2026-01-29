from pathlib import Path

import random
import string

from tkinter import *
from tkinter import messagebox

import json

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent

BACKGROUND_COLOR = "#B1DDC6"







window = Tk()
window.title("German words Flashcards")
window.config(padx=50, pady=50, bg= BACKGROUND_COLOR)

#cardbackimage = PhotoImage(file=str(SCRIPT_DIR / "card_back.png"))
#buttonback = Button(image=cardbackimage, highlightthickness=0)

canvas = Canvas(width=800, height=526, highlightthickness=0, background=BACKGROUND_COLOR)
cardfrontimage = PhotoImage(file=str(SCRIPT_DIR / "card_front.png"))
canvas.create_image(400, 263, image=cardfrontimage)  
canvas.grid(column=0, row=0,  columnspan=2)
canvas_lang = canvas.create_text(400, 150, text="German", font=("Ariel", 40, "italic"))
canvas_word = canvas.create_text(400, 263, text="WORD", font=("Ariel", 60, "bold"))

crossmarkimage = PhotoImage(file=str(SCRIPT_DIR / "wrong.png"))
button2 = Button(image=crossmarkimage, highlightthickness=0)
button2.grid(column=0, row=1)

checkmarkimage = PhotoImage(file=str(SCRIPT_DIR / "right.png"))
button1 = Button(image=checkmarkimage, highlightthickness=0)
button1.grid(column=1, row=1)



window.mainloop()

