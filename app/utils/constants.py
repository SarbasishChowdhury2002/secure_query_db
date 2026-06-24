from app.config import get_settings

settings = get_settings()

SEARCH_KEY = settings.SEARCH_KEY.encode()