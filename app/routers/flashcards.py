import json
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from supabase import Client
from typing import List, Optional, Any

from app.crud.crud import (
    update_flashcard, 
    create_flashcard_set, 
    delete_flashcard_set, 
    get_flashcard_set, 
    get_flashcard_sets, 
    get_flashcard_for_editing
)
from app.services.ollama import generate_flashcards_from_text
from app.schemas.schemas import (
    Flashcard, 
    FlashcardUpdate, 
    FlashcardSetCreate, 
    FlashcardSetDetail, 
    FlashcardSet, 
    FlashcardCreate
)
from app.dependencies import get_supabase_client, get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/sets/{set_id}", response_class=HTMLResponse)
async def set_detail_view(
    set_id: UUID,
    request: Request,
    supabase: Client = Depends(get_supabase_client),
    current_user: Any = Depends(get_current_user)  # ✅ ZMIENIONO typ
):
    """Wyświetla szczegóły zestawu fiszek z możliwością nauki"""
    try:
        # ✅ DEBUGOWANIE - sprawdź user_id
        print(f"🔍 DEBUG - current_user object: {current_user}")
        print(f"🔍 DEBUG - current_user.id: {current_user.id}")
        
        db_set = get_flashcard_set(
            supabase=supabase, 
            set_id=str(set_id),
            user_id=current_user.id
        )
        
        if db_set is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Zestaw fiszek nie został znaleziony"
            )
        
        flashcards_json = json.dumps([
            {
                "id": fc['id'], 
                "question": fc['question'], 
                "answer": fc['answer']
            } for fc in db_set.get('flashcards', [])
        ], ensure_ascii=False)
        
        return templates.TemplateResponse(
            "set_detail.html", 
            {
                "request": request, 
                "user": current_user, 
                "set": db_set, 
                "flashcards_json": flashcards_json
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Błąd podczas ładowania zestawu: {str(e)}"
        )

@router.get("/cards/{card_id}/edit", response_class=HTMLResponse)
async def edit_flashcard_view(
    card_id: UUID,
    request: Request,
    supabase: Client = Depends(get_supabase_client),
    current_user: Any = Depends(get_current_user)  # ✅ ZMIENIONO typ
):
    """Formularz edycji fiszki"""
    try:
        flashcard = get_flashcard_for_editing(supabase, str(card_id), current_user.id)
        
        if flashcard is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Fiszka nie została znaleziona lub nie masz uprawnień do jej edycji"
            )
            
        return templates.TemplateResponse(
            "edit_flashcard.html", 
            {
                "request": request, 
                "user": current_user, 
                "flashcard": flashcard
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Błąd podczas ładowania fiszki: {str(e)}"
        )

@router.post("/cards/{card_id}/edit", response_class=HTMLResponse)
async def edit_flashcard_post(
    card_id: UUID,
    request: Request,
    question: str = Form(...),
    answer: str = Form(...),
    supabase: Client = Depends(get_supabase_client),
    current_user: Any = Depends(get_current_user)  # ✅ ZMIENIONO typ
):
    """Zapisuje zmiany w fiszce"""
    try:
        flashcard = get_flashcard_for_editing(supabase, str(card_id), current_user.id)
        if not flashcard:
            return RedirectResponse(
                url="/dashboard", 
                status_code=status.HTTP_303_SEE_OTHER
            )

        question = question.strip()
        answer = answer.strip()
        
        if not question or not answer:
            return templates.TemplateResponse(
                "edit_flashcard.html",
                {
                    "request": request,
                    "user": current_user,
                    "flashcard": flashcard,
                    "error_message": "Pytanie i odpowiedź nie mogą być puste."
                },
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        flashcard_data = FlashcardUpdate(question=question, answer=answer)
        updated_flashcard = update_flashcard(
            supabase, 
            str(card_id), 
            current_user.id, 
            flashcard_data.model_dump(exclude_unset=True)
        )
        
        return RedirectResponse(
            url=f"/sets/{flashcard['set_id']}", 
            status_code=status.HTTP_303_SEE_OTHER
        )

    except HTTPException as e:
        flashcard = get_flashcard_for_editing(supabase, str(card_id), current_user.id)
        return templates.TemplateResponse(
            "edit_flashcard.html",
            {
                "request": request,
                "user": current_user,
                "flashcard": flashcard or {},
                "error_message": f"Błąd podczas zapisywania: {e.detail}"
            },
            status_code=e.status_code
        )

@router.get("/generate", response_class=HTMLResponse)
async def handle_generate_view_get(
    request: Request,
    current_user: Any = Depends(get_current_user)  # ✅ ZMIENIONO typ
):
    return templates.TemplateResponse(
        "generate.html", 
        {"request": request, "user": current_user}
    )

@router.post("/generate", response_class=HTMLResponse)
async def handle_generate_view_post(
    request: Request,
    supabase: Client = Depends(get_supabase_client),
    current_user: Any = Depends(get_current_user)  # ✅ ZMIENIONO typ
):
    try:
        # ✅ DEBUGOWANIE - sprawdź user_id na początku
        print(f"🔍 DEBUG POST /generate - current_user: {current_user}")
        print(f"🔍 DEBUG POST /generate - current_user.id: {current_user.id}")
        print(f"🔍 DEBUG POST /generate - user_id type: {type(current_user.id)}")
        
        form_data = await request.form()
        action = form_data.get("action")

        if action == "generate":
            text = form_data.get("text", "").strip()
            try:
                count = int(form_data.get("count", 5))
                count = max(1, min(count, 20))
            except (ValueError, TypeError):
                count = 5

            if not text:
                return templates.TemplateResponse(
                    "generate.html", 
                    {
                        "request": request, 
                        "user": current_user, 
                        "error_message": "Tekst źródłowy nie może być pusty."
                    }
                )

            try:
                generated_flashcards = await generate_flashcards_from_text(text, count)
                
                if not generated_flashcards:
                    return templates.TemplateResponse(
                        "generate.html", 
                        {
                            "request": request, 
                            "user": current_user, 
                            "error_message": "Nie udało się wygenerować fiszek z podanego tekstu."
                        }
                    )
                
                return templates.TemplateResponse(
                    "generate.html", 
                    {
                        "request": request, 
                        "user": current_user, 
                        "generated_flashcards": generated_flashcards,
                        "original_text": text,
                        "original_count": count
                    }
                )
                
            except HTTPException as e:
                return templates.TemplateResponse(
                    "generate.html", 
                    {
                        "request": request, 
                        "user": current_user, 
                        "error_message": e.detail
                    }
                )

        elif action == "save":
            set_name = form_data.get("name", "").strip()
            questions = form_data.getlist("questions")
            answers = form_data.getlist("answers")

            if not set_name:
                generated_flashcards = []
                for q, a in zip(questions, answers):
                    if q.strip() and a.strip():
                        generated_flashcards.append({"question": q.strip(), "answer": a.strip()})

                return templates.TemplateResponse(
                    "generate.html", 
                    {
                        "request": request, 
                        "user": current_user, 
                        "generated_flashcards": generated_flashcards, 
                        "error_message": "Nazwa zestawu nie może być pusta."
                    }
                )

            flashcards_to_create = []
            for q, a in zip(questions, answers):
                question = q.strip()
                answer = a.strip()
                if question and answer:
                    flashcards_to_create.append(FlashcardCreate(question=question, answer=answer))

            if not flashcards_to_create:
                return templates.TemplateResponse(
                    "generate.html", 
                    {
                        "request": request, 
                        "user": current_user, 
                        "error_message": "Musisz mieć przynajmniej jedną fiszkę z pytaniem i odpowiedzią."
                    }
                )

            try:
                # ✅ DEBUGOWANIE przed wywołaniem create_flashcard_set
                print(f"🔍 DEBUG przed create_flashcard_set - user_id: {current_user.id}")
                
                set_data = FlashcardSetCreate(name=set_name, flashcards=flashcards_to_create)
                created_set = create_flashcard_set(
                    supabase=supabase, 
                    set_data=set_data, 
                    user_id=current_user.id
                )
                
                return RedirectResponse(
                    url="/dashboard", 
                    status_code=status.HTTP_303_SEE_OTHER
                )
                
            except ValueError as e:
                generated_flashcards = []
                for q, a in zip(questions, answers):
                    if q.strip() and a.strip():
                        generated_flashcards.append({"question": q.strip(), "answer": a.strip()})

                return templates.TemplateResponse(
                    "generate.html", 
                    {
                        "request": request, 
                        "user": current_user, 
                        "generated_flashcards": generated_flashcards, 
                        "error_message": str(e)
                    }
                )

    except Exception as e:
        print(f"❌ UNEXPECTED ERROR in POST /generate: {e}")
        return templates.TemplateResponse(
            "generate.html", 
            {
                "request": request, 
                "user": current_user, 
                "error_message": f"Wystąpił nieoczekiwany błąd: {str(e)}"
            }
        )

@router.post("/sets/{set_id}/delete")
async def delete_flashcard_set_endpoint(
    set_id: UUID,
    supabase: Client = Depends(get_supabase_client),
    current_user: Any = Depends(get_current_user)  # ✅ ZMIENIONO typ
):
    try:
        delete_flashcard_set(supabase=supabase, set_id=str(set_id), user_id=current_user.id)
        return RedirectResponse(
            url="/dashboard", 
            status_code=status.HTTP_303_SEE_OTHER
        )
    except HTTPException as e:
        # Przekieruj na dashboard z informacją o błędzie
        return RedirectResponse(
            url=f"/dashboard?error_message={e.detail}", 
            status_code=status.HTTP_303_SEE_OTHER
        )
