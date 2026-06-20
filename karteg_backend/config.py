import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = "Karteg-Secret-Key"
    SESSION_PERMANENT = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = False
    DB_HOST = "localhost"
    DB_USER = "root"
    DB_PASSWORD = ""
    DB_NAME = "karteg_db"

    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"

    JSON_SORT_KEYS = False