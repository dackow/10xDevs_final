from supabase import Client
from app.schemas.schemas import FlashcardSetCreate, FlashcardCreate
from fastapi import HTTPException, status
from typing import Union, Dict, Any, List
import uuid

def create_flashcard_set(supabase: Client, set_data: FlashcardSetCreate, user_id: str) -> Dict[str, Any]:
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
    response = supabase.table('flashcard_sets').select('*, flashcards(*)').eq('id', set_id).eq('user_id', user_id).execute()
    if not response.data:
        return None
    return response.data[0]

def get_flashcard_sets(supabase: Client, user_id: str):
    response = supabase.table('flashcard_sets').select('*').eq('user_id', user_id).execute()
    return response.data or []

def get_flashcard_for_editing(supabase: Client, card_id: Union[str, int], user_id: str):
    response = supabase.table('flashcards').select('*, flashcard_sets!inner(user_id)').eq('id', card_id).execute()
    if not response.data or response.data[0]['flashcard_sets']['user_id'] != user_id:
        return None
    return response.data[0]

def update_flashcard(supabase: Client, card_id: Union[str, int], user_id: str, flashcard_data: dict):
    card_to_edit = get_flashcard_for_editing(supabase, card_id, user_id)
    if not card_to_edit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flashcard not found")

    response = supabase.table('flashcards').update(flashcard_data).eq('id', card_id).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update flashcard")
    return response.data[0]

def delete_flashcard_set(supabase: Client, set_id: Union[str, int], user_id: str):
    response = supabase.table('flashcard_sets')\
        .select('*')\
        .eq('id', set_id)\
        .eq('user_id', user_id)\
        .execute()
    
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flashcard set not found")

    try:
        delete_response = supabase.table('flashcard_sets')\
            .delete()\
            .eq('id', set_id)\
            .eq('user_id', user_id)\
            .execute()
        
        if not delete_response.data:
            pass
        
        return {"message": "Flashcard set deleted successfully"}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Nie udało się usunąć zestawu fiszek: {str(e)}"
        )