from fastapi import APIRouter, Depends, HTTPException, status
from typing import Any, Dict, List, Optional

from app.schemas.schemas import FlashcardGenerateRequest, AIGenerationResponse, ToolDefinition, ToolExecuteRequest, ToolExecuteResponse
# from app.dependencies import get_current_user # Remove this import

from app.services.ollama import generate_flashcards_from_text

router = APIRouter()

# Placeholder for the actual tool function
async def generate_flashcards_ai_function(
    text: str,
    count: int,
    # current_user: Any, # Remove this parameter
    # supabase: Any # Assuming supabase client might be needed, though not directly used in this specific function
) -> Dict:
    try:
        # Call the existing Ollama service function
        flashcards_data = await generate_flashcards_from_text(text, count)
        # Ensure the output matches the AIGenerationResponse schema
        return {"flashcards": flashcards_data}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error generating flashcards: {str(e)}")

TOOLS_MAP = {
    "generateFlashcardsAI": generate_flashcards_ai_function
}

@router.get("/tools/definitions", response_model=List[ToolDefinition])
async def get_tool_definitions():
    definitions = []
    # For generateFlashcardsAI
    definitions.append(ToolDefinition(
        name="generateFlashcardsAI",
        description="Generates flashcards (question-answer pairs) from provided source text and a specified number of flashcards.",
        input_schema=FlashcardGenerateRequest.model_json_schema(),
        output_schema=AIGenerationResponse.model_json_schema()
    ))
    return definitions

@router.post("/tools/execute", response_model=ToolExecuteResponse)
async def execute_tool(
    request: ToolExecuteRequest,
    # current_user: Any = Depends(get_current_user) # Remove this dependency
):
    tool_name = request.tool_name
    parameters = request.parameters

    if tool_name not in TOOLS_MAP:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tool '{tool_name}' not found."
        )

    tool_function = TOOLS_MAP[tool_name]

    try:
        # Validate parameters using the appropriate Pydantic model
        if tool_name == "generateFlashcardsAI":
            validated_params = FlashcardGenerateRequest(**parameters)
            result = await tool_function(
                text=validated_params.text,
                count=validated_params.count,
                # current_user=current_user # Remove this parameter from the call
            )
        else:
            # Handle other tools if they are added in the future
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Tool '{tool_name}' not supported for execution.")

        return ToolExecuteResponse(content=result)
    except HTTPException as e:
        return ToolExecuteResponse(error={"message": e.detail, "code": str(e.status_code)})
    except Exception as e:
        return ToolExecuteResponse(error={"message": f"An unexpected error occurred: {str(e)}", "code": "500"})