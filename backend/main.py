from fastapi import FastAPI

app = FastAPI(
    title="LegacyMind API",
    description="AI-powered Legacy Code Modernization Platform",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Welcome to LegacyMind",
        "status": "Backend is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }