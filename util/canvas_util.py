import requests
import json
from util import config_util

BASE_URL = "https://dexterschools.instructure.com/api/v1"

def get_notification_course_id():
    return config_util.get_config_item("default_canvas_course")

def send_announcement(course_id, title, message, is_published=True):
    token = config_util.get_config_item("canvas_token")

    PARAMS = {
            "access_token": token,
            "title": title,
            "message": message,
            "published": is_published,
            "is_announcement": True
        }

    r = requests.post(f"{BASE_URL}/courses/{course_id}/discussion_topics", PARAMS)
    return r.json()
