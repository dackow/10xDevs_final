import sys
print("sys.path before imports:", sys.path)
from fastapi import FastAPI
from app.routers import auth, flashcards

app = FastAPI()

app.include_router(auth.router)
app.include_router(flashcards.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Flashcard Generator API"}
