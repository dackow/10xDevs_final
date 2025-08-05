from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models
from app.crud.crud import update_flashcard
from app.schemas.schemas import Flashcard, FlashcardUpdate
from app.dependencies import get_db, get_current_user

router = APIRouter()

@router.put("/flashcards/{card_id}", response_model=Flashcard)
def update_flashcard_endpoint(card_id: int, flashcard_data: FlashcardUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """
    Aktualizuje istniejącą fiszkę.

    Args:
        card_id (int): ID fiszki do zaktualizowania.
        flashcard_data (FlashcardUpdate): Nowe dane dla fiszki (pytanie i odpowiedź).
        db (Session): Sesja bazy danych.
        current_user (models.User): Aktualnie zalogowany użytkownik.

    Returns:
        Flashcard: Zaktualizowana fiszka.

    Raises:
        HTTPException: Jeśli fiszka nie zostanie znaleziona lub użytkownik nie ma uprawnień.
    """
    db_flashcard = update_flashcard(db=db, card_id=card_id, user_id=current_user.id, flashcard_data=flashcard_data.dict())
    if db_flashcard is None:
        raise HTTPException(status_code=404, detail="Flashcard not found or you don't have permission to edit it")
    return db_flashcard

@router.post("/generate")
def generate_flashcards():
    # Logic for generating flashcards
    pass

@router.post("/sets")
def save_flashcard_set():
    # Logic for saving a flashcard set
    pass

@router.get("/sets")
def get_flashcard_sets():
    # Logic for getting all flashcard sets
    pass

@router.put("/sets/{set_id}")
def update_flashcard_set(set_id: int):
    # Logic for updating a flashcard set
    pass

@router.delete("/sets/{set_id}")
def delete_flashcard_set(set_id: int):
    # Logic for deleting a flashcard set
    pass
