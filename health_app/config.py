#Configuration settings for the app (e.g., API keys, debug mode).

import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key')
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    GOOGLE_PLACES_API_KEY = os.environ.get('GOOGLE_PLACES_API_KEY')
