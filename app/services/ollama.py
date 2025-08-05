import httpx
import json
import os
from typing import List
from fastapi import HTTPException, status
from app.schemas.schemas import FlashcardCreate
from dotenv import load_dotenv
from json_repair import repair_json

load_dotenv()

OLLAMA_API_URL = os.getenv("OLLAMA_API_URL")
OLLAMA_MODEL_NAME = os.getenv("OLLAMA_MODEL_NAME")

if not OLLAMA_API_URL:
    raise ValueError("OLLAMA_API_URL environment variable not set.")

if not OLLAMA_MODEL_NAME:
    raise ValueError("OLLAMA_MODEL_NAME environment variable not set.")

async def generate_flashcards_from_text(text: str, count: int) -> List[FlashcardCreate]:
    prompt = f"""
    Generate {count} flashcards (question and answer) from the following text.
    YOUR RESPONSE MUST BE A JSON ARRAY ONLY. DO NOT INCLUDE ANY OTHER TEXT OR EXPLANATIONS.
    Each object in the array must have 'question' and 'answer' keys.
    Example:
    [
      {{"question": "What is the capital of France?", "answer": "Paris"}},
      {{"question": "What is the highest mountain in the world?", "answer": "Mount Everest"}}
    ]

    Text:
    {text}
    """

    payload = {
        "model": OLLAMA_MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        
    }

    max_retries = 3
    for attempt in range(max_retries):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(OLLAMA_API_URL, json=payload, timeout=60.0)
                response.raise_for_status() # Raise an exception for 4xx or 5xx responses

                response_data = response.json()
                generated_content = response_data.get("response")

                

                if not generated_content or not generated_content.strip():
                    if attempt < max_retries - 1:
                        print(f"Ollama returned empty content on attempt {attempt + 1}. Retrying...")
                        continue
                    else:
                        raise HTTPException(
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Ollama did not return any generated content or it was empty after multiple attempts."
                        )

                # Attempt to repair and parse the JSON array from the generated content
                print(f"DEBUG: generated_content repr: {repr(generated_content)}")
                try:
                    repaired_json_string = repair_json(str(generated_content).strip())
                    flashcards_data = json.loads(repaired_json_string)
                    return _validate_and_create_flashcards(flashcards_data)
                except (json.JSONDecodeError, ValueError) as parse_exc:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"Failed to parse JSON from Ollama's response even after repair: {parse_exc}. Raw content: {generated_content}"
                    )

        except (json.JSONDecodeError, httpx.RequestError, httpx.HTTPStatusError) as exc:
            if attempt < max_retries - 1:
                print(f"Error on attempt {attempt + 1}. Retrying Ollama call... Error: {exc}")
                continue
            else:
                if isinstance(exc, json.JSONDecodeError):
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"Ollama returned malformed JSON after {max_retries} attempts: {generated_content}. Error: {exc}"
                    )
                elif isinstance(exc, httpx.RequestError):
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"Could not connect to Ollama service after {max_retries} attempts: {exc}"
                    )
                elif isinstance(exc, httpx.HTTPStatusError):
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"Error from Ollama service after {max_retries} attempts: {exc.response.status_code} - {exc.response.text}"
                    )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred: {e}"
            )
    
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Failed to generate flashcards after multiple attempts due to unknown error."
    )

def _validate_and_create_flashcards(flashcards_data: List[dict]) -> List[FlashcardCreate]:
    if not isinstance(flashcards_data, list):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ollama returned an invalid flashcard format (not a list)."
        )
    
    flashcards = []
    for item in flashcards_data:
        if not isinstance(item, dict) or "question" not in item or "answer" not in item:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ollama returned an invalid flashcard format (missing question/answer)."
            )
        flashcards.append(FlashcardCreate(question=item["question"], answer=item["answer"]))
    
    return flashcards
