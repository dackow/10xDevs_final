from typing import List, Any
from supabase import Client
from app.schemas.schemas import FlashcardCreate, FlashcardSetCreate, FlashcardSet
from app.services.ollama import generate_flashcards_from_text as ollama_generate
from app.crud import crud
from app.exceptions import GenerationFailedError, SaveFailedError
from fastapi import HTTPException, status

async def generate_flashcards(text: str, count: int) -> List[FlashcardCreate]:
    """
    Generates flashcards from the given text using the Ollama service.
    """
    try:
        generated_flashcards = await ollama_generate(text, count)
        if not generated_flashcards:
            raise GenerationFailedError("Ollama did not return any generated content.")
        return generated_flashcards
    except Exception as e:
        raise GenerationFailedError(f"Failed to generate flashcards: {e}")


def save_flashcard_set(db: Client, set_data: FlashcardSetCreate, user_id: str) -> FlashcardSet:
    """
    Saves a new flashcard set to the database.
    """
    set_name = set_data.name.strip()
    if not set_name:
        raise SaveFailedError("Set name cannot be empty.")

    existing_set = db.table('flashcard_sets').select('id').eq('user_id', user_id).eq('name', set_name).execute()
    if existing_set.data:
        raise SaveFailedError(f"A set with the name '{set_name}' already exists.")

    try:
        created_set = crud.create_flashcard_set(db, set_data, user_id)
        return FlashcardSet(**created_set)
    except Exception as e:
        raise SaveFailedError(f"Failed to save flashcard set: {e}")

def update_flashcard(db: Client, card_id: str, user_id: str, flashcard_data: dict) -> Any:
    """
    Updates a flashcard in the database.
    """
    return crud.update_flashcard(db, card_id, user_id, flashcard_data)

def delete_flashcard_set(db: Client, set_id: str, user_id: str) -> None:
    """
    Deletes a flashcard set from the database.
    """
    crud.delete_flashcard_set(db, set_id, user_id)
