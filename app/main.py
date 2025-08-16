import sys
from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from supabase import Client
from app.dependencies import get_current_user, get_supabase_client
from app.routers import auth, flashcards
from app.crud.crud import get_flashcard_sets
from typing import Any
from app.exceptions import GenerationFailedError, SaveFailedError

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")

app.include_router(auth.router)
app.include_router(flashcards.router)

@app.exception_handler(GenerationFailedError)
async def generation_failed_exception_handler(request: Request, exc: GenerationFailedError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

@app.exception_handler(SaveFailedError)
async def save_failed_exception_handler(request: Request, exc: SaveFailedError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )


@app.get("/")
def read_root():
    return RedirectResponse(url="/login")

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    supabase: Client = Depends(get_supabase_client),
    current_user: Any = Depends(get_current_user)
):
    flashcard_sets = get_flashcard_sets( supabase, current_user.id)
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": current_user, "flashcard_sets": flashcard_sets})