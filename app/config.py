import os
from dotenv import load_dotenv

# Wybór pliku .env przez ENV_FILE (fallback na ".env")
#ENV_FILE = os.getenv("ENV_FILE", ".env")
load_dotenv()

# Klucze i konfiguracja
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

# (opcjonalnie) zmienne dla Ollama, jeśli używasz:
# OLLAMA_API_URL = os.getenv("OLLAMA_API_URL")
# OLLAMA_MODEL_NAME = os.getenv("OLLAMA_MODEL_NAME")
