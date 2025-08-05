from fastapi import APIRouter, Depends, HTTPException, status, Query, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app import models
from app.crud.crud import update_flashcard, create_flashcard_set, delete_flashcard_set, get_flashcard_set, get_flashcard_sets, get_flashcard_for_editing
from app.schemas.schemas import Flashcard, FlashcardUpdate, FlashcardSetCreate, FlashcardSetDetail, FlashcardSet
from app.dependencies import get_db, get_current_user
import logging

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/sets/{set_id}", response_class=HTMLResponse)
async def set_detail_view(
    set_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_set = get_flashcard_set(db=db, set_id=set_id, user_id=current_user.id)
    if db_set is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flashcard set not found")
    return templates.TemplateResponse("set_detail.html", {"request": request, "user": current_user, "set": db_set})

@router.get("/cards/{card_id}/edit", response_class=HTMLResponse)
async def edit_flashcard_view(
    card_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    flashcard = get_flashcard_for_editing(db, card_id, current_user.id)
    if flashcard is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flashcard not found or you don't have permission to edit it")
    return templates.TemplateResponse("edit_flashcard.html", {"request": request, "user": current_user, "flashcard": flashcard})

@router.post("/cards/{card_id}/edit", response_class=HTMLResponse)
async def edit_flashcard_post(
    card_id: int,
    request: Request,
    question: str = Form(...),
    answer: str = Form(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    flashcard = get_flashcard_for_editing(db, card_id, current_user.id)
    if not flashcard:
        # This case should ideally not be reached if UI checks are in place,
        # but as a fallback, redirect to the dashboard.
        return RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)

    if not question or not answer:
        # Re-render the edit form with an error message
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

    try:
        flashcard_data = FlashcardUpdate(question=question, answer=answer)
        updated_flashcard = update_flashcard(db, card_id, current_user.id, flashcard_data.model_dump())
        
        # After the update attempt, always redirect to the set detail page.
        # The original flashcard object (before update) has the set_id.
        return RedirectResponse(url=f"/sets/{flashcard.set_id}", status_code=status.HTTP_303_SEE_OTHER)

    except HTTPException as e:
        # Handle potential database or other errors by re-rendering the form with an error.
        return templates.TemplateResponse(
            "edit_flashcard.html",
            {
                "request": request,
                "user": current_user,
                "flashcard": flashcard,
                "error_message": e.detail
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.get("/generate", response_class=HTMLResponse)
async def handle_generate_view_get(
    request: Request,
    current_user: models.User = Depends(get_current_user)
):
    return templates.TemplateResponse("generate.html", {"request": request, "user": current_user})

@router.post("/generate", response_class=HTMLResponse)
async def handle_generate_view_post(
    request: Request,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    form_data = await request.form()
    action = form_data.get("action")

    if action == "generate":
        text = form_data.get("text")
        count = int(form_data.get("count", 5))

        if not text:
            return templates.TemplateResponse("generate.html", {"request": request, "user": current_user, "error_message": "Tekst źródłowy nie może być pusty."})

        try:
            generated_flashcards = await generate_flashcards_from_text(text, count)
            return templates.TemplateResponse("generate.html", {"request": request, "user": current_user, "generated_flashcards": generated_flashcards})
        except HTTPException as e:
            return templates.TemplateResponse("generate.html", {"request": request, "user": current_user, "error_message": e.detail})
        except Exception as e:
            return templates.TemplateResponse("generate.html", {"request": request, "user": current_user, "error_message": f"Wystąpił nieoczekiwany błąd podczas generowania fiszek: {e}"})

    elif action == "save":
        set_name = form_data.get("name")
        questions = form_data.getlist("questions")
        answers = form_data.getlist("answers")

        if not set_name:
            generated_flashcards = []
            for q, a in zip(questions, answers):
                generated_flashcards.append({"question": q, "answer": a})

            return templates.TemplateResponse("generate.html", {"request": request, "user": current_user, "generated_flashcards": generated_flashcards, "error_message": "Nazwa zestawu nie może być pusta."})

        flashcards_to_create = []
        for q, a in zip(questions, answers):
            flashcards_to_create.append(Flashcard(question=q, answer=a))
        
        try:
            set_data = FlashcardSetCreate(name=set_name, flashcards=flashcards_to_create)
            create_flashcard_set(db=db, set_data=set_data, user_id=current_user.id)
            return RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
        except ValueError as e:
            generated_flashcards = []
            for q, a in zip(questions, answers):
                generated_flashcards.append({"question": q, "answer": a})

            return templates.TemplateResponse("generate.html", {"request": request, "user": current_user, "generated_flashcards": generated_flashcards, "error_message": str(e)})

        except HTTPException as e:
            generated_flashcards = []
            for q, a in zip(questions, answers):
                generated_flashcards.append({"question": q, "answer": a})

            return templates.TemplateResponse("generate.html", {"request": request, "user": current_user, "generated_flashcards": generated_flashcards, "error_message": e.detail})

    return templates.TemplateResponse("generate.html", {"request": request, "user": current_user, "error_message": "Nieznana akcja."})
