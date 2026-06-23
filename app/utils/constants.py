
import os
from dotenv import load_dotenv

load_dotenv()

SEARCH_KEY = os.getenv("SEARCH_KEY", "fallback-key").encode()