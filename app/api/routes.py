from fastapi import APIRouter, HTTPException
from .schemas import QuestionRequest
from app.services.langchain_service import get_answer_from_chain

# Create a new router object
router = APIRouter()

@router.post("/ask", summary="Ask a question", description="Receives a question and context, returns an answer from Gemini.")
def ask_question(request: QuestionRequest):
    """
    This endpoint takes a question and an optional context,
    and returns the model's answer by calling the LangChain service.
    """
    try:
        result = get_answer_from_chain(context=request.context, question=request.question)
        return {"answer": result.get('text', 'No answer found.')}
    except Exception as e:
        # Handle potential errors
        raise HTTPException(status_code=500, detail=str(e))

