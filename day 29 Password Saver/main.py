# ---------------------------- CONSTANTS ------------------------------- #
import os
from pathlib import Path

import random
import string

from tkinter import *
from tkinter import messagebox

import pyperclip

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():


    letters = string.ascii_letters
    numbers = string.digits
    symbols = string.punctuation

    password_letters = [random.choice(letters) for _ in range(random.randint(8, 10))]
    password_symbols = [random.choice(symbols) for _ in range(random.randint(2, 4))]
    password_numbers = [random.choice(numbers) for _ in range(random.randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    random.shuffle(password_list)

    password = ''.join(password_list)
    password_text.delete("1.0", END)
    password_text.insert(END, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #

def save_password():
    if website_text.get("1.0", END).strip() == "" or password_text.get("1.0", END).strip() == "":
        messagebox.showinfo(title="Oops", message="Please make sure no fields are empty.")
        return

    is_ok = messagebox.askokcancel(title=website_text.get("1.0", END).strip(),
                                   message=f"These are the details entered: \nEmail: {email_text.get('1.0', END).strip()} \nPassword: {password_text.get('1.0', END).strip()} \nIs it ok to save?")
    if is_ok:
        with open(SCRIPT_DIR / "passwords.txt", "a") as file:
            file.write(f"{website_text.get('1.0', END).strip()} | {email_text.get('1.0', END).strip()} | {password_text.get('1.0', END).strip()}\n")
        website_text.delete("1.0", END)
        email_text.delete("1.0", END)
        password_text.delete("1.0", END)
        messagebox.showinfo(title="Success", message="Password saved successfully!")
# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Generator")
window.config(padx=120, pady=50)

canvas = Canvas(width=200, height=200, highlightthickness=0)

logo_img = PhotoImage(file=str(SCRIPT_DIR / "logo.png"))
canvas.create_image(100, 100, image=logo_img)  
canvas.grid(column=1, row=1)

website_label = Label(text="Website")
website_label.grid(column=0, row=2)
website_label.config(pady=5)


website_text = Text(height=1, width=37)
website_text.focus()
website_text.insert(END, "")
print(website_text.get("1.0", END))
website_text.grid(column=1, row=2,  columnspan=3)


email_label = Label(text="Email")
email_label.grid(column=0, row=3)
email_label.config(pady=5)


email_text = Text(height=1, width=37)
email_text.focus()
email_text.insert(END, "")
print(email_text.get("1.0", END))
email_text.grid(column=1, row=3, columnspan=3)

password_label = Label(text="Password")
password_label.grid(column=0, row=4)
password_label.config(pady=5)

password_text = Text(height=1, width=23)
password_text.focus()
password_text.insert(END, "")
print(password_text.get("1.0", END))
password_text.grid(column=1, row=4)

generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(column=2, row=4)


add_button = Button(text="Add", width = 35, command=save_password)
add_button.grid(column=1, row=5, columnspan=3)


window.mainloop()

