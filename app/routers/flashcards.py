from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app import models
from app.crud.crud import update_flashcard, create_flashcard_set, delete_flashcard_set, get_flashcard_set, get_flashcard_sets
from app.schemas.schemas import Flashcard, FlashcardUpdate, FlashcardSetCreate, FlashcardSetDetail, FlashcardSet
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
    db_flashcard = update_flashcard(db=db, card_id=card_id, user_id=current_user.id, flashcard_data=flashcard_data.model_dump())
    if db_flashcard is None:
        raise HTTPException(status_code=404, detail="Flashcard not found or you don't have permission to edit it")
    return db_flashcard

from app.schemas.schemas import AIGenerationRequest, AIGenerationResponse
from app.services.ollama import generate_flashcards_from_text

@router.post("/ai/generate-flashcards", response_model=AIGenerationResponse)
async def generate_flashcards_endpoint(
    request: AIGenerationRequest,
    current_user: models.User = Depends(get_current_user)
):
    """
    Generuje fiszki za pomocą modelu AI (Ollama) na podstawie dostarczonego tekstu źródłowego.
    """
    try:
        flashcards = await generate_flashcards_from_text(request.text, request.count)
        return AIGenerationResponse(flashcards=flashcards)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred during flashcard generation: {e}"
        )

@router.post("/sets", response_model=FlashcardSetDetail, status_code=status.HTTP_201_CREATED)
def create_flashcard_set_endpoint(
    set_data: FlashcardSetCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Tworzy nowy zestaw fiszek dla uwierzytelnionego użytkownika.

    Args:
        set_data (FlashcardSetCreate): Dane do utworzenia zestawu fiszek, w tym nazwa i lista fiszek.
        db (Session): Sesja bazy danych.
        current_user (models.User): Aktualnie zalogowany użytkownik.

    Returns:
        FlashcardSetDetail: Utworzony zestaw fiszek wraz z przypisanymi fiszkami.

    Raises:
        HTTPException: Jeśli zestaw o tej samej nazwie już istnieje dla danego użytkownika (400 Bad Request),
                       lub jeśli dane wejściowe są nieprawidłowe (422 Unprocessable Entity).
    """
    try:
        db_flashcard_set = create_flashcard_set(db=db, set_data=set_data, user_id=current_user.id)
        return db_flashcard_set
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/sets/{set_id}", response_model=FlashcardSetDetail)
def get_flashcard_set_endpoint(set_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """
    Pobiera szczegółowe informacje o pojedynczym zestawie fiszek.

    Args:
        set_id (int): ID zestawu fiszek do pobrania.
        db (Session): Sesja bazy danych.
        current_user (models.User): Aktualnie zalogowany użytkownik.

    Returns:
        FlashcardSetDetail: Szczegółowe informacje o zestawie fiszek.

    Raises:
        HTTPException: Jeśli zestaw nie zostanie znaleziony (404 Not Found).
    """
    db_flashcard_set = get_flashcard_set(db=db, set_id=set_id, user_id=current_user.id)
    if db_flashcard_set is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flashcard set not found")
    return db_flashcard_set

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app import models
from app.crud.crud import update_flashcard, create_flashcard_set, delete_flashcard_set, get_flashcard_set, get_flashcard_sets
from app.schemas.schemas import Flashcard, FlashcardUpdate, FlashcardSetCreate, FlashcardSetDetail, FlashcardSet
from app.dependencies import get_db, get_current_user


@router.get("/sets", response_model=list[FlashcardSet])
def get_flashcard_sets_endpoint(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=0, le=100),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Pobiera listę wszystkich zestawów fiszek należących do uwierzytelnionego użytkownika.
    Obsługuje paginację.

    Args:
        skip (int): Liczba rekordów do pominięcia (dla paginacji).
        limit (int): Maksymalna liczba rekordów do zwrócenia.
        db (Session): Sesja bazy danych.
        current_user (models.User): Aktualnie zalogowany użytkownik.

    Returns:
        List[FlashcardSet]: Lista zestawów fiszek.
    """
    flashcard_sets = get_flashcard_sets(db=db, user_id=current_user.id, skip=skip, limit=limit)
    return flashcard_sets

@router.put("/sets/{set_id}")
def update_flashcard_set(set_id: int):
    # Logic for updating a flashcard set
    pass

@router.delete("/sets/{set_id}")
def delete_flashcard_set_endpoint(set_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """
    Usuwa zestaw fiszek na podstawie jego ID.

    Args:
        set_id (int): ID zestawu fiszek do usunięcia.
        db (Session): Sesja bazy danych.
        current_user (models.User): Aktualnie zalogowany użytkownik.

    Returns:
        dict: Komunikat o sukcesie.

    Raises:
        HTTPException: Jeśli zestaw nie zostanie znaleziony (404 Not Found),
                       lub użytkownik nie ma uprawnień do usunięcia (403 Forbidden).
    """
    return delete_flashcard_set(db=db, set_id=set_id, user_id=current_user.id)
