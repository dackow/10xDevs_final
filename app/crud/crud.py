from sqlalchemy.orm import Session
from . import models, schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(username=user.username, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_flashcard_sets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.FlashcardSet).offset(skip).limit(limit).all()

def create_flashcard_set(db: Session, flashcard_set: schemas.FlashcardSetCreate, user_id: int):
    db_flashcard_set = models.FlashcardSet(**flashcard_set.dict(), owner_id=user_id)
    db.add(db_flashcard_set)
    db.commit()
    db.refresh(db_flashcard_set)
    return db_flashcard_set
