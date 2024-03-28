
import sys
import os
myDir = os.getcwd()

print(myDir)
sys.path.append(myDir)

from utility.gupshup import Gupshup

gs = Gupshup()

# print(gs.send_text_message("test from api","919004189363"))
print(gs.send_button_message("test from api",["success","not yet"],"919004189363"))
list_data = {
            "header":"Test1",
            "body":"body-text",
            "button_text":"Click me",
            "list_sections":[
                {
                    "title" : "Choose me",
                    "options" : ["1","2","3"]
                },
                {
                    "title" : "Choose me 2nd time",
                    "options" : ["1","2","3"]
                }
            ]

        }
# print(gs.send_list_message(list_data,"919004189363"))