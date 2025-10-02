from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from app.core.config import settings

# --- LangChain Setup ---
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.5, google_api_key=settings.GOOGLE_API_KEY)

# Define the prompt template
template = """
Based on the following context, please provide a concise answer to the question.
If the context does not contain the answer, say you don't have enough information.

Context: {context}
Question: {question}

Answer:
"""
prompt = PromptTemplate(template=template, input_variables=["context", "question"])

# Create the LangChain chain
llm_chain = LLMChain(prompt=prompt, llm=llm)

def get_answer_from_chain(context: str, question: str) -> dict:
    return llm_chain.invoke({"context": context, "question": question})

