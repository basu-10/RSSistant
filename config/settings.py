from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CSV_DIR = "data/rss_data_files"
FILTERS_FILE = "user_data/user_filters.json"
USER_AGENT = "Mozilla/5.0 (Linux; Android 9; Pixel 3 XL) AppleWebKit/537.36 ..."
