from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.repositories import router as repositories_router
from app.api.routes.analysis import router as analysis_router

app = FastAPI(
    title="LegacyMind API",
    description="AI-powered Legacy Code Modernization Platform",
    version="1.0.0"
)

# Allow communication with the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Register API routes
app.include_router(repositories_router)
app.include_router(analysis_router)

@app.get("/")
def root():
    return {
        "message": "Welcome to LegacyMind",
        "status": "Backend is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "project": "LegacyMind"
    }
