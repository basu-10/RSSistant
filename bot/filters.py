import os
import json
from config.settings import FILTERS_FILE

def load_user_filters():
    if os.path.exists(FILTERS_FILE):
        with open(FILTERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_user_filters(data):
    with open(FILTERS_FILE, "w") as f:
        json.dump(data, f)

user_filters = load_user_filters()
