from pydantic import BaseModel, Field

# --- Pydantic Model for Request Body ---
# This defines the expected structure of the JSON payload for the /ask endpoint.
class QuestionRequest(BaseModel):
    question: str
    context: str = Field(
        default="Mount Everest is the Earth's highest mountain above sea level, located in the Himalayas.",
        title="Context",
        description="The context provided to the model to help answer the question."
    )

