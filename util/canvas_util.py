import requests #Allows data to be recieved and sent to databases
import json #creates and accesses json files that contain dictionaries for attributes of an object
from util import config_util #imports configuration to access certain values from keys

BASE_URL = "https://dexterschools.instructure.com/api/v1" #The base URL when posting data to the server that is manipulated to the right link

def get_notification_course_id():  #Parses through the JSON dictionary, finds the key "default canvas course", and sends back the value
    return config_util.get_config_item("default_canvas_course")

def send_announcement(course_id, title, message, is_published=True): #A function requiring the ID, title, message, and published is True
    token = config_util.get_config_item("canvas_token") #accesses the Canvas token in order to access the API

    PARAMS = {  #The information necessary that gets sent along with the link
            "access_token": token,  
            "title": title,
            "message": message,
            "published": is_published,
            "is_announcement": True 
        }

    r = requests.post(f"{BASE_URL}/courses/{course_id}/discussion_topics", PARAMS)
    return r.json()
