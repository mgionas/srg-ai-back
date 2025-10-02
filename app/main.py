from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Imports are now relative because main.py is inside the 'app' package
from .api import routes
from .core.config import settings

# --- FastAPI App Initialization ---
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="SRG AI Agent",
    version="1.0.0",
)

# --- CORS (Cross-Origin Resource Sharing) Middleware ---
origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Include API Router ---
app.include_router(routes.router, prefix="/api/v1")