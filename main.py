from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import APP_NAME
from .database import Base, engine, SessionLocal
from .create_admin import ensure_admin
from .routers import auth, documents, admin
@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        ensure_admin(db)
    yield
app = FastAPI(title=APP_NAME, version="1.0.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=False,
                   allow_methods=["*"], allow_headers=["*"])
@app.get("/")
def root():
    return {"message": "Nangarhar University Library API is running", "docs": "/docs"}
@app.get("/health")
def health():
    return {"status": "ok"}
app.include_router(auth.router)
app.include_router(documents.router)
app.include_router(admin.router)
