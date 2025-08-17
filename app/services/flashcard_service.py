"""
This module provides services for managing flashcards, including generation via AI,
and CRUD operations for flashcard sets and individual flashcards.
It orchestrates interactions between routers, CRUD operations, and external AI models.
"""

from typing import List, Any
from supabase import Client
from app.schemas.schemas import FlashcardCreate, FlashcardSetCreate, FlashcardSet
from app.services.ollama import generate_flashcards_from_text as ollama_generate
from app.crud import crud
from app.exceptions import GenerationFailedError, SaveFailedError
from fastapi import HTTPException, status

async def generate_flashcards(text: str, count: int) -> List[FlashcardCreate]:
    """Generates flashcards from the given text using the Ollama service.

    :param text: The source text from which to generate flashcards.
    :type text: str
    :param count: The desired number of flashcards to generate.
    :type count: int
    :raises GenerationFailedError: If the Ollama service fails to return generated content.
    :returns: A list of generated flashcards.
    :rtype: List[FlashcardCreate]
    :dependencies:
        - `app.services.ollama`: For AI-powered text generation.
        - `app.exceptions.GenerationFailedError`: Custom exception for generation failures.
    """
    try:
        generated_flashcards = await ollama_generate(text, count)
        if not generated_flashcards:
            raise GenerationFailedError("Ollama did not return any generated content.")
        return generated_flashcards
    except Exception as e:
        raise GenerationFailedError(f"Failed to generate flashcards: {e}")


def save_flashcard_set(db: Client, set_data: FlashcardSetCreate, user_id: str) -> FlashcardSet:
    """Saves a new flashcard set to the database.

    This function handles the creation of a new flashcard set, including its associated
    flashcards, and ensures that set names are unique for a given user.

    :param db: The Supabase client instance.
    :type db: Client
    :param set_data: The data for the flashcard set to be created, including its name and flashcards.
    :type set_data: FlashcardSetCreate
    :param user_id: The ID of the user who owns the flashcard set.
    :type user_id: str
    :raises SaveFailedError: If the set name is empty, a set with the same name already exists for the user, or if the database operation fails.
    :returns: The created flashcard set object.
    :rtype: FlashcardSet
    :dependencies:
        - `app.crud.crud`: For database CRUD operations.
        - `app.exceptions.SaveFailedError`: Custom exception for save failures.
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
    """Updates an existing flashcard in the database.

    :param db: The Supabase client instance.
    :type db: Client
    :param card_id: The ID of the flashcard to update.
    :type card_id: str
    :param user_id: The ID of the user who owns the flashcard. Used for authorization.
    :type user_id: str
    :param flashcard_data: A dictionary containing the fields to update (e.g., 'question', 'answer').
    :type flashcard_data: dict
    :returns: The updated flashcard data.
    :rtype: Any
    :dependencies:
        - `app.crud.crud`: For database CRUD operations.
    """
    return crud.update_flashcard(db, card_id, user_id, flashcard_data)

def delete_flashcard_set(db: Client, set_id: str, user_id: str) -> None:
    """Deletes a flashcard set from the database.

    This function deletes a flashcard set and all associated flashcards.
    Authorization is performed based on the user ID.

    :param db: The Supabase client instance.
    :type db: Client
    :param set_id: The ID of the flashcard set to delete.
    :type set_id: str
    :param user_id: The ID of the user who owns the flashcard set. Used for authorization.
    :type user_id: str
    :returns: None
    :rtype: None
    :dependencies:
        - `app.crud.crud`: For database CRUD operations.
    """
    crud.delete_flashcard_set(db, set_id, user_id)
