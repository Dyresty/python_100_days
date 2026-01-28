
# ---------------------------- CONSTANTS ------------------------------- #
from pathlib import Path
from tkinter import *

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent

PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25 * 60
SHORT_BREAK_MIN = 5 * 60
LONG_BREAK_MIN = 20 * 60
reps = -1
timer_id = None  # Track scheduled callback to cancel it
#GUI is event driven programming. 
#Code only runs when an event happens, like a button click.

# ---------------------------- TIMER RESET ------------------------------- # 




def button_end_clicked():
    global reps, timer_id
    if timer_id is not None:
        window.after_cancel(timer_id)
        timer_id = None
    canvas.itemconfig(canvas_text, text="00:00")
    timer_label.config(text="Start Work!", fg=GREEN)
    reps = -1
    check_marks.config(text='')

# ---------------------------- TIMER MECHANISM ------------------------------- # 

def button_start_clicked(i):
    global reps
    if i==0 and reps!=-1:
        return
    if reps == -1:
        reps = 0
    
    if reps % 8 == 7:
        count_down(LONG_BREAK_MIN, "long_break")
        timer_label.config(text="Long Break", fg=RED)
    elif (reps % 8) % 2 == 0:
        count_down(WORK_MIN, "work")
        timer_label.config(text="Work", fg=GREEN)
    else:
        count_down(SHORT_BREAK_MIN, "break")
        timer_label.config(text="Short Break", fg=PINK)
    reps += 1
# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 

def count_down(count, phase_type):
    global timer_id
    minutes = count // 60
    seconds = count % 60
    canvas.itemconfig(canvas_text, text=f"{minutes:02d}:{seconds:02d}")
    if count>0:
        timer_id = window.after(1000, count_down, count-1, phase_type)
    if count==0:
        timer_id = None
        # Update checkmarks after work session completes
        if phase_type == "work":
            work_sessions_completed = (reps // 2) + 1
            check_marks.config(text='✔' * work_sessions_completed)
        # Auto-start next session
        window.after(1000, lambda: button_start_clicked(1))

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Pomodoro")
window.config(padx=50, pady=50, bg=YELLOW)

title = Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 50))
title.grid(column=1, row=0)

timer_label = Label(text="Start Work!", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 30), width=15)
timer_label.grid(column=1, row=1)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file=str(SCRIPT_DIR / "tomato.png"))
canvas.create_image(100, 112, image=tomato_img)  
canvas_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=2)

button_start = Button(text="Start", command=lambda: button_start_clicked(0))
button_start.config(highlightthickness=0, padx=20, pady=5)
button_start.grid(column=0, row=3)

button_end = Button(text="Reset", command = button_end_clicked)
button_end.config(highlightthickness=0, padx=20, pady=5)
button_end.grid(column=2, row=3)

check_marks = Label(fg=GREEN, bg=YELLOW, font=(FONT_NAME, 20))
check_marks.grid(column=1, row=4)


window.mainloop()