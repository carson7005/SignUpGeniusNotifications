import requests
import json

BASE_URL = "https://dexterschools.instructure.com/api/v1"

def get_notification_course_id():
    token_file = open("canvas_token.json")
    data = json.load(token_file)
    course_id = data["default_course"]
    token_file.close()

    return course_id

def send_announcement(course_id, title, message, is_published=True):
    token_file = open("canvas_token.json")
    data = json.load(token_file)
    token = data["token"]

    PARAMS = {
            "access_token": token,
            "title": title,
            "message": message,
            "published": is_published,
            "is_announcement": True
        }

    r = requests.post(f"{BASE_URL}/courses/{course_id}/discussion_topics", PARAMS)
    token_file.close()
    return r.json()