from pydantic import BaseModel

class FlashcardBase(BaseModel):
    question: str
    answer: str

class FlashcardCreate(FlashcardBase):
    pass

class Flashcard(FlashcardBase):
    id: int
    flashcard_set_id: int

    class Config:
        orm_mode = True

class FlashcardSetBase(BaseModel):
    title: str

class FlashcardSetCreate(FlashcardSetBase):
    pass

class FlashcardSet(FlashcardSetBase):
    id: int
    owner_id: int
    flashcards: list[Flashcard] = []

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    flashcard_sets: list[FlashcardSet] = []

    class Config:
        orm_mode = True
