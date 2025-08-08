from supabase import Client
from app.schemas.schemas import FlashcardSetCreate, FlashcardCreate
from fastapi import HTTPException, status
from typing import Union, Dict, Any, List
import uuid

def create_flashcard_set(supabase: Client, set_data: FlashcardSetCreate, user_id: str) -> Dict[str, Any]:
    # ✅ ROZSZERZONE DEBUGOWANIE
    print(f"🔍 DEBUG create_flashcard_set - Received user_id: '{user_id}'")
    print(f"🔍 DEBUG create_flashcard_set - user_id type: {type(user_id)}")
    print(f"🔍 DEBUG create_flashcard_set - user_id is None: {user_id is None}")
    print(f"🔍 DEBUG create_flashcard_set - user_id is empty string: {user_id == ''}")
    print(f"🔍 DEBUG create_flashcard_set - set_data.name: '{set_data.name}'")
    
    if not user_id:
        print("❌ user_id is empty or None!")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Brak user_id")
    
    set_name = set_data.name.strip()
    if not set_name:
        raise ValueError("Nazwa zestawu nie może być pusta.")
    
    print(f"📋 Creating set '{set_name}' for user: {user_id}")
    
    # Sprawdź duplikaty
    existing_set = supabase.table('flashcard_sets')\
        .select('id')\
        .eq('user_id', user_id)\
        .eq('name', set_name)\
        .execute()
    
    if existing_set.data:
        raise ValueError(f"Zestaw o nazwie '{set_name}' już istnieje.")
    
    # ✅ DEBUGOWANIE DANYCH DO WSTAWIENIA
    new_set_data = {
        'name': set_name,
        'user_id': user_id
    }
    print(f"🔍 DEBUG - Data to insert: {new_set_data}")
    
    try:
        set_response = supabase.table('flashcard_sets')\
            .insert(new_set_data)\
            .execute()
        
        # ✅ DEBUGOWANIE ODPOWIEDZI
        print(f"🔍 DEBUG - Supabase insert response: {set_response}")
        
        if not set_response.data:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Nie udało się utworzyć zestawu")
        
        new_set = set_response.data[0]
        new_set_id = new_set['id']
        
        print(f"✅ Set created: {new_set['name']}")
        
        # Dodaj fiszki
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
                    print(f"✅ Added {len(inserted_flashcards)} flashcards")
                else:
                    # Rollback
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
        print(f"❌ ERROR in create_flashcard_set: {e}")
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
    response = supabase.table('flashcard_sets').select('*').eq('id', set_id).eq('user_id', user_id).execute()
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flashcard set not found")

    delete_response = supabase.table('flashcard_sets').delete().eq('id', set_id).execute()
    
    if not delete_response.data:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Nie udało się usunąć zestawu fiszek.")
        
    return {"message": "Flashcard set deleted successfully"}
