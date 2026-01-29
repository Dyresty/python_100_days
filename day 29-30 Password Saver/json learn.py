#JSON stands for JavaScript Object Notation

# json.dumps() -Write
# json.loads() - Read
# json.update() - Update

# json.read() - read json file
# json.write() - write to json file


from pathlib import Path
SCRIPT_DIR = Path(__file__).parent

import json
new_data = {
    "website":{
        "email":"blah blah",
        "password":"bleh bleh"
    }
}
with open((str(SCRIPT_DIR / "data.json")), "w") as file:
    json.dump(new_data, file, indent = 4)


with open("data.json", "r") as file:
    data = json.load(file)
    print(data)
    print(type(data))

new_data = {
    "website":{
        "email":"blah blah",
        "password":"bluh bluh"
    }
}

with open((str(SCRIPT_DIR / "data.json")), "r") as file:
    #read old data
    data = json.load(file)
    #updating old data with new data
    data.update(new_data)  
with open((str(SCRIPT_DIR / "data.json")), "w")  as file:
    #Write the updated data 
    json.dump(data, file, indent = 4)
    print(data)
