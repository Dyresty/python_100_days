"""
#FileNotFound
with open("non_existent_file.txt", "r") as file:
    content = file.read()

#KeyError
my_dict = {"a": 1, "b": 2}
value = my_dict["c"]

#IndexError
my_list = [1, 2, 3]
element = my_list[5]

#ZeroDivisionError
result = 10 / 0

#TypeError
number = 5 + "10"

#AttributeError
my_string = "Hello"
my_string.append(" World")

#ValueError
number = int("abc")

#ImportError
from non_existent_module import some_function

NameError - Using a variable that doesn't exist
RecursionError - Exceeded maximum recursion depth
AssertionError - Assertion statement failed
EOFError - End of file reached unexpectedly
RuntimeError - General runtime error
NotImplementedError - Method not implemented
SyntaxError - Invalid syntax
IndentationError - Incorrect indentation
MemoryError - Out of memory
OverflowError - Number too large
StopIteration - Iterator exhausted
ModuleNotFoundError - Specific module not found (subclass of ImportError)
UnicodeError - Unicode encoding/decoding issues
TimeoutError - Operation timed out
ConnectionError - Connection-related error

"""

# Example of handling exceptions

import os
from pathlib import Path

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent


#Try - Something that might cause an error
#Except - Do this if there is an error
#Else - Do this if there were no errors
#Finally - Do this no matter what
try:
    with open(str(SCRIPT_DIR / "passwords.txt"), "r") as file:
        content = file.read()
        a = {"key": "value"}
        print(a["non_existent_key"])
except FileNotFoundError:
    print("The file was not found.")
except KeyError:
    print("The specified key does not exist in the dictionary.")
else:
    print(content)
    file.close()
finally:
    print("Execution completed.")

# Raising your own exceptions
height = float(input("Height: "))
weight = float(input("Weight: "))

if height > 3:
    raise ValueError("Human height should not be over 3 meters.")

bmi = weight / height ** 2
print(bmi)
