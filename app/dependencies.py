from fastapi import Depends, HTTPException, status, Request
from app.config import SUPABASE_URL, SUPABASE_KEY
from supabase import create_client, Client
from typing import Any

def get_supabase_client() -> Client:
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise Exception("Supabase configuration missing")
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def get_current_user(request: Request, supabase: Client = Depends(get_supabase_client)) -> Any:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token = request.cookies.get("access_token")
    if not token:
        raise credentials_exception
    
    if token.startswith("Bearer "):
        token = token[len("Bearer "):]

    try:
        user_response = supabase.auth.get_user(token)
        if user_response.user is None:
            raise credentials_exception
        
        # ✅ DEBUGOWANIE - sprawdź strukturę użytkownika Supabase
        print(f"🔍 DEBUG - Supabase user: {user_response.user}")
        print(f"🔍 DEBUG - User ID: {user_response.user.id}")
        print(f"🔍 DEBUG - User attributes: {dir(user_response.user)}")
        
        return user_response.user
        
    except Exception as e:
        print(f"❌ Error in get_current_user: {e}")
        raise credentials_exception
