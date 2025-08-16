from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Optional
from uuid import UUID # Import UUID

# =============================================================================
# 1. SCHEMATY DLA FISZEK (FLASHCARDS)
# =============================================================================

class FlashcardBase(BaseModel):
    """Podstawowy schemat dla fiszki, zawiera wspolne pola."""
    question: str
    answer: str

class FlashcardCreate(FlashcardBase):
    """Schemat uzywany do tworzenia nowej fiszki (np. przez AI)."""
    pass

class FlashcardUpdate(FlashcardBase):
    """Schemat uzywany do aktualizacji istniejacej fiszki."""
    pass

class Flashcard(FlashcardBase):
    """Pelny schemat fiszki, uzywany w odpowiedziach API (DTO)."""
    id: Optional[UUID] = None
    set_id: Optional[UUID] = None
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    model_config = ConfigDict(from_attributes=True)

# =============================================================================
# 2. SCHEMATY DLA ZESTAWOW FISZEK (FLASHCARD SETS)
# =============================================================================

class FlashcardSetBase(BaseModel):
    """Podstawowy schemat dla zestawu fiszek."""
    name: str

class FlashcardSetCreate(FlashcardSetBase):
    """Schemat uzywany do tworzenia nowego zestawu wraz z fiszkami (Command Model)."""
    flashcards: List[FlashcardCreate]

class FlashcardSet(FlashcardSetBase):
    """Schemat reprezentujacy zestaw na liscie (widok podsumowania)."""
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class FlashcardSetDetail(FlashcardSet):
    """Schemat reprezentujacy pelny, szczegolowy widok zestawu z fiszkami (DTO)."""
    flashcards: List[Flashcard] = []

# =============================================================================
# 3. SCHEMATY DLA UZYTKOWNIKOW (USERS)
# =============================================================================

class UserBase(BaseModel):
    """Podstawowy schemat uzytkownika."""
    username: str

class UserCreate(UserBase):
    """Schemat uzywany do tworzenia nowego uzytkownika (Command Model)."""
    password: str

class User(UserBase):
    """Schemat uzytkownika zwracany przez API (DTO), bez hasla."""
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

# =============================================================================
# 4. SCHEMATY DLA MECHANIZMOW POMOCNICZYCH (AUTH, AI)
# =============================================================================

class Token(BaseModel):
    """Schemat dla tokena uwierzytelniajacego JWT."""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Schemat dla danych zakodowanych w tokenie."""
    username: Optional[str] = None

class AIGenerationRequest(BaseModel):
    """Schemat dla zadania wygenerowania fiszek przez AI (Command Model)."""
    text: str
    count: int

class AIGenerationResponse(BaseModel):
    """Schemat dla odpowiedzi z wygenerowanymi fiszkami (DTO)."""
    flashcards: List[FlashcardCreate]

class FlashcardGenerateRequest(BaseModel):
    text: str
    count: int

class FlashcardSaveRequest(BaseModel):
    name: str
    flashcards: List[FlashcardCreate]