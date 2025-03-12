import os
from dotenv import load_dotenv

load_dotenv()

CSV_FILE = os.environ.get("CSV_FILE")
DB_URL = os.environ.get("DB_URL")
DB_URI = os.environ.get("DB_URI")
