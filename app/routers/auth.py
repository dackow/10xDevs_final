from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from supabase import Client

from app.dependencies import get_supabase_client

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")

@router.post("/login")
async def login_user(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    supabase: Client = Depends(get_supabase_client)
):
    if not email or not password:
        return templates.TemplateResponse(request=request, name="login.html", context={"error_message": "Email i hasło są wymagane."})

    try:
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})

        if not response.session or not response.session.access_token:
            return templates.TemplateResponse(request=request, name="login.html", context={"error_message": "Błąd autoryzacji - nieprawidłowy email lub hasło."})

        access_token = response.session.access_token

        redirect_response = RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
        redirect_response.set_cookie(
            key="access_token",
            value=f"Bearer {access_token}",
            httponly=True,
            samesite="Lax",
            secure=True,
            max_age=3600
        )
        return redirect_response

    except Exception as e:
        return templates.TemplateResponse(request=request, name="login.html", context={"error_message": "Wystąpił błąd podczas logowania."})

@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse(request=request, name="register.html")

@router.post("/register", response_class=HTMLResponse)
async def register_user(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    supabase: Client = Depends(get_supabase_client)
):
    if not email or not password:
        return templates.TemplateResponse(request=request, name="register.html", context={"error_message": "Email i hasło są wymagane."})

    try:
        response = supabase.auth.admin.create_user({"email": email, "password": password, "email_confirm": True})
        print(response)
        if not response.user:
            return templates.TemplateResponse(request=request, name="register.html", context={"error_message": "Nie udało się zarejestrować użytkownika."})
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        print(e)
        return templates.TemplateResponse(request=request, name="register.html", context={"error_message": str(e)})

@router.post("/logout")
async def logout_user(supabase: Client = Depends(get_supabase_client)):
    try:
        supabase.auth.sign_out()
    except Exception as e:
        pass
    response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("access_token")
    return response
