"""
This module defines the API routes and handlers for user authentication.
It includes endpoints for user login, registration, and logout, interacting with Supabase for authentication.
"""

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

@router.post("/register")
async def register_user(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    supabase: Client = Depends(get_supabase_client)
):
    if not email or not password:
        return templates.TemplateResponse(request=request, name="register.html", context={"error_message": "Email i hasło są wymagane."})

    try:
        # Create user in auth.users
        auth_response = supabase.auth.admin.create_user({"email": email, "password": password, "email_confirm": True})
        if not auth_response.user:
            return templates.TemplateResponse(request=request, name="register.html", context={"error_message": "Nie udało się zarejestrować użytkownika w systemie autoryzacji."})
        
        user_id = auth_response.user.id
        
        # Insert user into public.users
        user_data = {"id": user_id, "email": email}
        insert_response = supabase.table("users").insert(user_data).execute()

        # Check for errors during insert
        if insert_response.data is None and insert_response.error is not None:
            # If the insert fails, we should probably delete the user from auth.users to keep things clean
            supabase.auth.admin.delete_user(user_id)
            return templates.TemplateResponse(request=request, name="register.html", context={"error_message": f"Nie udało się zapisać użytkownika w bazie danych: {insert_response.error.message}"})


        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        # Check if the error is due to an existing user
        if "A user with this email address has already been registered" in str(e):
            error_message = "Użytkownik o tym adresie email już istnieje."
        else:
            error_message = f"Wystąpił błąd podczas rejestracji: {str(e)}"
        return templates.TemplateResponse(request=request, name="register.html", context={"error_message": error_message})

@router.post("/logout")
async def logout_user(supabase: Client = Depends(get_supabase_client)):
    try:
        supabase.auth.sign_out()
    except Exception as e:
        pass
    response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("access_token")
    return response