import os
APP_NAME = os.getenv("APP_NAME", "Nangarhar University Library API")
SECRET_KEY = os.getenv("SECRET_KEY", "local-development-key-change-me")
ALGORITHM = "HS256"
ACCESS_TOKEN_MINUTES = int(os.getenv("ACCESS_TOKEN_MINUTES", "720"))
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./library.db")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "").strip().lower()
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "")
