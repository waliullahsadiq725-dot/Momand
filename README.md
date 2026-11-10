# Nangarhar University Library API

## Deploy to Render
1. Upload every file and folder in this ZIP to the ROOT of a new GitHub repository.
2. In Render, create a Web Service and connect that repository.
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables: `SECRET_KEY` (long random value), `ADMIN_EMAIL`, `ADMIN_PASSWORD`.
6. For production persistence, create a Render PostgreSQL database and set `DATABASE_URL` to its Internal Database URL.
7. Deploy. Test `/health`, then open `/docs`.

## Local run
Use Python 3.12, run `pip install -r requirements.txt`, then `uvicorn app.main:app --reload`.
Keep the `app/` folder and its `__init__.py` files. Never upload passwords or `.env` to GitHub.
SQLite is for local testing; use PostgreSQL on Render because the service filesystem is ephemeral.
