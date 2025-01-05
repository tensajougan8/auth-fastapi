from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.db.connection import engine
import app.models.base as base
from app.api import auth as auth_router
from app.api import users as user_router
from app.api import coins as crypto_router
from app.api import weather as weather_router

base.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Authentication App")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key='your-secret-key-here'  # Use a secure secret key
)

# Include routers
app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(crypto_router.router)
app.include_router(weather_router.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)