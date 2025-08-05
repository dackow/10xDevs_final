from datetime import datetime, UTC
from sqlalchemy.orm import Session, joinedload
from app import models
from app.schemas.schemas import UserCreate, FlashcardSetCreate, FlashcardUpdate
from fastapi import HTTPException, status


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

from app.services import auth_service

def create_user(db: Session, user: UserCreate):
    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    hashed_password = auth_service.get_password_hash(user.password)
    db_user = models.User(username=user.username, password_hash=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_flashcard_set(db: Session, set_data: FlashcardSetCreate, user_id: int):
    # Sprawdzenie unikalności nazwy zestawu dla danego użytkownika
    existing_set = db.query(models.FlashcardSet).filter(
        models.FlashcardSet.user_id == user_id,
        models.FlashcardSet.name == set_data.name
    ).first()
    if existing_set:
        # Zgłoś wyjątek, który zostanie obsłużony w routerze
        raise ValueError("Flashcard set with this name already exists for this user.")

    # Utworzenie nowego zestawu fiszek
    db_flashcard_set = models.FlashcardSet(name=set_data.name, user_id=user_id)
    db.add(db_flashcard_set)
    db.flush()  # Upewnij się, że db_flashcard_set.id jest dostępne

    # Dodanie fiszek do zestawu
    for flashcard_data in set_data.flashcards:
        db_flashcard = models.Flashcard(
            question=flashcard_data.question,
            answer=flashcard_data.answer,
            set_id=db_flashcard_set.id
        )
        db.add(db_flashcard)

    db.commit()
    db.refresh(db_flashcard_set)
    # Załaduj relację flashcards, aby była dostępna w zwróconym obiekcie
    db.refresh(db_flashcard_set)
    return db_flashcard_set


def get_flashcard_set(db: Session, set_id: int, user_id: int):
    return db.query(models.FlashcardSet).options(joinedload(models.FlashcardSet.flashcards)).filter(
        models.FlashcardSet.id == set_id,
        models.FlashcardSet.user_id == user_id
    ).first()


def get_flashcard_sets(db: Session, user_id: int):
    return db.query(models.FlashcardSet).filter(models.FlashcardSet.user_id == user_id).all()


def get_flashcard_for_editing(db: Session, card_id: int, user_id: int):
    """
    Retrieves a flashcard for editing, verifying ownership.

    Args:
        db: The database session.
        card_id: The ID of the flashcard.
        user_id: The ID of the user.

    Returns:
        The flashcard if it exists and belongs to the user, otherwise None.
    """
    return (
        db.query(models.Flashcard)
        .join(models.FlashcardSet)
        .filter(models.Flashcard.id == card_id, models.FlashcardSet.user_id == user_id)
        .first()
    )

def update_flashcard(db: Session, card_id: int, user_id: int, flashcard_data: dict):
    """
    Aktualizuje fiszkę na podstawie jej ID, weryfikując, czy użytkownik jest właścicielem.
    """
    # Pobierz fiszkę z joinem do zestawu, weryfikując jednocześnie własność
    db_flashcard = db.query(models.Flashcard).join(models.FlashcardSet).filter(
        models.Flashcard.id == card_id,
        models.FlashcardSet.user_id == user_id
    ).first()

    if not db_flashcard:
        return None

    # Aktualizacja danych
    for key, value in flashcard_data.items():
        if hasattr(db_flashcard, key):
            setattr(db_flashcard, key, value)

    # Ustaw updated_at na aktualny czas
    db_flashcard.updated_at = datetime.now(UTC)
    
    db.commit()
    db.refresh(db_flashcard)
    return db_flashcard


def delete_flashcard_set(db: Session, set_id: int, user_id: int):
    db_set = db.query(models.FlashcardSet).filter(models.FlashcardSet.id == set_id).first()

    if not db_set:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flashcard set not found")

    if db_set.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this flashcard set")

    db.delete(db_set)
    db.commit()
    return {"message": "Flashcard set deleted successfully"}
