from sqlalchemy.orm import Session
from app import models
from app.schemas.schemas import UserCreate, FlashcardSetCreate

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

from app.services import auth_service

def create_user(db: Session, user: UserCreate):
    hashed_password = auth_service.get_password_hash(user.password)
    db_user = models.User(username=user.username, password_hash=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_flashcard_sets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.FlashcardSet).offset(skip).limit(limit).all()

def create_flashcard_set(db: Session, flashcard_set: FlashcardSetCreate, user_id: int):
    db_flashcard_set = models.FlashcardSet(**flashcard_set.dict(), user_id=user_id)
    db.add(db_flashcard_set)
    db.commit()
    db.refresh(db_flashcard_set)
    return db_flashcard_set

def update_flashcard(db: Session, card_id: int, user_id: int, flashcard_data: dict):
    """
    Aktualizuje fiszkę na podstawie jej ID, weryfikując, czy użytkownik jest właścicielem.

    Args:
        db (Session): Sesja bazy danych.
        card_id (int): ID fiszki do aktualizacji.
        user_id (int): ID użytkownika próbującego dokonać aktualizacji.
        flashcard_data (dict): Słownik z danymi do aktualizacji (question, answer).

    Returns:
        models.Flashcard: Zaktualizowany obiekt fiszki lub None, jeśli nie znaleziono lub brak uprawnień.
    """
    db_flashcard = db.query(models.Flashcard).filter(models.Flashcard.id == card_id).first()

    if not db_flashcard:
        return None

    # Sprawdzenie uprawnień
    if db_flashcard.set.user_id != user_id:
        return None # Lub rzucić wyjątek autoryzacji

    # Aktualizacja danych
    for key, value in flashcard_data.items():
        setattr(db_flashcard, key, value)

    db.commit()
    db.refresh(db_flashcard)
    return db_flashcard
