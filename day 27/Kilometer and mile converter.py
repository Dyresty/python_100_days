import tkinter as tk

window = tk.Tk()
window.title("Kilometer and Mile Converter")
window.minsize(width=600, height=450)
window.config(padx=50, pady=50)

# Global variables
conversion_mode = 1  # 1 = Mile to Kilometer, 0 = Kilometer to Mile

# Title Label
title_label = tk.Label(text="Mile to Kilometer", font=("Arial", 24, "bold"))
title_label.grid(column=1, row=0, columnspan=1, padx=20, pady=20)

# Input Label
input_label = tk.Label(text="Enter value:")
input_label.grid(column=0, row=1, padx=10)

# Entry widget
input_entry = tk.Entry(width=15)
input_entry.grid(column=1, row=1, padx=10)

# Toggle button to switch conversion mode
def toggle_conversion():
    global conversion_mode
    conversion_mode = 1 - conversion_mode
    if conversion_mode == 1:
        title_label.config(text="Mile to Kilometer")
    else:
        title_label.config(text="Kilometer to Mile")
    result_label.config(text="Enter a value and click Convert")
    input_entry.delete(0, tk.END)

toggle_button = tk.Button(text="Toggle Mode", command=toggle_conversion, width=15)
toggle_button.grid(column=2, row=1, padx=10)

# Result label
result_label = tk.Label(text="Enter a value and click Convert", font=("Arial", 14))
result_label.grid(column=0, row=2, columnspan=3, padx=20, pady=20)

# Convert button
def convert():
    try:
        value = float(input_entry.get())
        if conversion_mode == 1:
            # Mile to Kilometer
            converted = value * 1.60934
            result_label.config(text=f"{value} Miles = {converted:.2f} Kilometers")
        else:
            # Kilometer to Mile
            converted = value / 1.60934
            result_label.config(text=f"{value} Kilometers = {converted:.2f} Miles")
    except ValueError:
        result_label.config(text="Please enter a valid number")

convert_button = tk.Button(text="Convert", command=convert, width=15, bg="lightblue")
convert_button.grid(column=1, row=3, columnspan=2, padx=10, pady=10)

# Clear button
def clear_all():
    input_entry.delete(0, tk.END)
    result_label.config(text="Enter a value and click Convert")

clear_button = tk.Button(text="Clear", command=clear_all, width=15)
clear_button.grid(column=0, row=3, padx=10, pady=10)

window.mainloop()