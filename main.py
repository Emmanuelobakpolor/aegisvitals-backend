from fastapi import FastAPI
from app.api.auth import router as auth_router

app = FastAPI(title="AegisVitals API")

app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "AegisVitals API running"}
