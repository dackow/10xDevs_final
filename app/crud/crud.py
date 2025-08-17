"""
This module provides Create, Read, Update, and Delete (CRUD) operations
for interacting with the Supabase database tables related to flashcards and flashcard sets.
It encapsulates direct database access logic.
"""

from supabase import Client
from app.schemas.schemas import FlashcardSetCreate, FlashcardCreate
from fastapi import HTTPException, status
from typing import Union, Dict, Any, List
import uuid

def create_flashcard_set(supabase: Client, set_data: FlashcardSetCreate, user_id: str) -> Dict[str, Any]:
    """Creates a new flashcard set and its associated flashcards in the database.

    Ensures that the user ID is provided and that the set name is unique for the user.
    If flashcards are provided in `set_data`, they are also inserted and linked to the new set.

    :param supabase: The Supabase client instance.
    :type supabase: Client
    :param set_data: The data for the flashcard set to be created, including its name and a list of flashcards.
    :type set_data: FlashcardSetCreate
    :param user_id: The ID of the user who is creating the flashcard set.
    :type user_id: str
    :raises HTTPException: If `user_id` is missing, if the set cannot be created, or if flashcards cannot be added.
    :raises ValueError: If the set name is empty or a set with the same name already exists for the user.
    :returns: A dictionary representing the newly created flashcard set, including its ID and inserted flashcards.
    :rtype: Dict[str, Any]
    :dependencies:
        - `supabase`: For database operations.
        - `app.schemas.schemas.FlashcardSetCreate`: For input data validation.
    """
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Brak user_id")
    
    set_name = set_data.name.strip()
    if not set_name:
        raise ValueError("Nazwa zestawu nie może być pusta.")
    
    existing_set = supabase.table('flashcard_sets')\
        .select('id')\
        .eq('user_id', user_id)\
        .eq('name', set_name)\
        .execute()
    
    if existing_set.data:
        raise ValueError(f"Zestaw o nazwie '{set_name}' już istnieje.")
    
    new_set_data = {
        'name': set_name,
        'user_id': user_id
    }
    
    try:
        set_response = supabase.table('flashcard_sets')\
            .insert(new_set_data)\
            .execute()
        
        if not set_response.data:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Nie udało się utworzyć zestawu")
        
        new_set = set_response.data[0]
        new_set_id = new_set['id']
        
        inserted_flashcards = []
        if set_data.flashcards:
            flashcards_to_insert = []
            for fc in set_data.flashcards:
                question = fc.question.strip()
                answer = fc.answer.strip()
                if question and answer:
                    flashcards_to_insert.append({
                        'question': question,
                        'answer': answer,
                        'set_id': new_set_id
                    })
            
            if flashcards_to_insert:
                flashcards_response = supabase.table('flashcards')\
                    .insert(flashcards_to_insert)\
                    .execute()
                
                if flashcards_response.data:
                    inserted_flashcards = flashcards_response.data
                else:
                    supabase.table('flashcard_sets').delete().eq('id', new_set_id).execute()
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Nie udało się dodać fiszek")
        
        return {
            'id': new_set['id'],
            'name': new_set['name'],
            'user_id': new_set['user_id'],
            'created_at': new_set.get('created_at'),
            'flashcards': inserted_flashcards
        }
        
    except Exception as e:
        if "duplicate key" in str(e).lower():
            raise ValueError(f"Zestaw o nazwie '{set_name}' już istnieje.")
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Błąd: {str(e)}")

def get_flashcard_set(supabase: Client, set_id: Union[str, int], user_id: str) -> Union[Dict[str, Any], None]:
    """Retrieves a single flashcard set by its ID, ensuring it belongs to the specified user.

    Includes all associated flashcards within the returned set data.

    :param supabase: The Supabase client instance.
    :type supabase: Client
    :param set_id: The ID of the flashcard set to retrieve.
    :type set_id: Union[str, int]
    :param user_id: The ID of the user who owns the flashcard set.
    :type user_id: str
    :returns: A dictionary representing the flashcard set, or `None` if not found or not owned by the user.
    :rtype: Union[Dict[str, Any], None]
    :dependencies:
        - `supabase`: For database operations.
    """
    response = supabase.table('flashcard_sets').select('*, flashcards(*)').eq('id', set_id).eq('user_id', user_id).execute()
    if not response.data:
        return None
    return response.data[0]

def get_flashcard_sets(supabase: Client, user_id: str):
    """Retrieves all flashcard sets for a given user.

    :param supabase: The Supabase client instance.
    :type supabase: Client
    :param user_id: The ID of the user whose flashcard sets are to be retrieved.
    :type user_id: str
    :returns: A list of dictionaries, each representing a flashcard set. Returns an empty list if no sets are found.
    :rtype: List[Dict[str, Any]]
    :dependencies:
        - `supabase`: For database operations.
    """
    response = supabase.table('flashcard_sets').select('*').eq('user_id', user_id).execute()
    return response.data or []

def get_flashcard_for_editing(supabase: Client, card_id: Union[str, int], user_id: str):
    """Retrieves a specific flashcard for editing, ensuring it belongs to the specified user.

    This function checks ownership by joining with the `flashcard_sets` table.

    :param supabase: The Supabase client instance.
    :type supabase: Client
    :param card_id: The ID of the flashcard to retrieve.
    :type card_id: Union[str, int]
    :param user_id: The ID of the user who owns the flashcard.
    :type user_id: str
    :returns: A dictionary representing the flashcard or `None` if not found or not owned by the user.
    :rtype: Union[Dict[str, Any], None]
    :dependencies:
        - `supabase`: For database operations.
    """
    response = supabase.table('flashcards').select('*, flashcard_sets!inner(user_id)').eq('id', card_id).execute()
    if not response.data or response.data[0]['flashcard_sets']['user_id'] != user_id:
        return None
    return response.data[0]

def update_flashcard(supabase: Client, card_id: Union[str, int], user_id: str, flashcard_data: dict):
    """Updates an existing flashcard in the database.

    First, it verifies that the flashcard exists and is owned by the specified user.

    :param supabase: The Supabase client instance.
    :type supabase: Client
    :param card_id: The ID of the flashcard to update.
    :type card_id: Union[str, int]
    :param user_id: The ID of the user who owns the flashcard. Used for authorization.
    :type user_id: str
    :param flashcard_data: A dictionary containing the fields to update (e.g., 'question', 'answer').
    :type flashcard_data: dict
    :raises HTTPException: If the flashcard is not found or if the update operation fails.
    :returns: A dictionary representing the updated flashcard.
    :rtype: Dict[str, Any]
    :dependencies:
        - `supabase`: For database operations.
    """
    card_to_edit = get_flashcard_for_editing(supabase, card_id, user_id)
    if not card_to_edit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flashcard not found")

    response = supabase.table('flashcards').update(flashcard_data).eq('id', card_id).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update flashcard")
    return response.data[0]

def delete_flashcard_set(supabase: Client, set_id: Union[str, int], user_id: str):
    """Deletes a flashcard set and all its associated flashcards from the database.

    This function first verifies that the flashcard set exists and is owned by the specified user
    before proceeding with the deletion.

    :param supabase: The Supabase client instance.
    :type supabase: Client
    :param set_id: The ID of the flashcard set to delete.
    :type set_id: Union[str, int]
    :param user_id: The ID of the user who owns the flashcard set. Used for authorization.
    :type user_id: str
    :raises HTTPException: If the flashcard set is not found or if the delete operation fails.
    :returns: A dictionary with a success message.
    :rtype: Dict[str, str]
    :dependencies:
        - `supabase`: For database operations.
    """
    response = supabase.table('flashcard_sets')\
        .select('*')\
        .eq('id', set_id)\
        .eq('user_id', user_id)\
        .execute()
    
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flashcard set not found")

    try:
        delete_response = supabase.table('flashcard_sets')\
            .delete()
            .eq('id', set_id)
            .eq('user_id', user_id)
            .execute()
        
        if not delete_response.data:
            pass
        
        return {"message": "Flashcard set deleted successfully"}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Nie udało się usunąć zestawu fiszek: {str(e)}"
        )
