from fastapi import APIRouter, HTTPException
from google.cloud import bigquery  # Import the BigQuery client
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


@router.get("/test-bigquery", summary="Count nexio_sessions Records", description="Tests the BigQuery connection")
def test_bigquery_connection():
    try:
        client = bigquery.Client()

        # Query
        query = """
            SELECT COUNT(*) as total_records
            FROM `silk-hospitality-x.casino_rag.nexio_sessions`
        """

        query_job = client.query(query)
        results = query_job.result()

        # get the first row
        row = next(iter(results))
        record_count = row.total_records

        return {
            "status": "ok",
            "message": "Successfully queried nexio_sessions table.",
            "record_count": record_count
        }

    except Exception as e:
        # Catch Errors
        raise HTTPException(
            status_code=500,
            detail=f"Failed to query BigQuery table: {str(e)}"
        )