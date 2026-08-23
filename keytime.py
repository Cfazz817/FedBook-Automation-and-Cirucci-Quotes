import os
from dotenv import load_dotenv

load_dotenv()

PAGE_ID = os.getenv("PAGE_ID")
FB_ACCESS = os.getenv("FB_ACCESS")
DEFAULT_MESSAGE = os.getenv("DEFAULT_MESSAGE")
APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")
SHORT_LIVED_TOKEN = os.getenv("SHORT_LIVED_TOKEN")
