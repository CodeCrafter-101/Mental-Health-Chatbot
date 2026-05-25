from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from helpline_support import (
    contains_distress_keywords,
    get_safety_message   
)

from chat_logs import log_chat  # optional

app = FastAPI()

# CORS (frontend connection)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class ChatRequest(BaseModel):
    session_id: str
    query: str

# Health check
@app.get("/")
def home():
    return {"message": "working"}

# Main chat endpoint
@app.post("/chat")
def chat(request: ChatRequest):
    session_id = request.session_id
    user_query = request.query

    # Distress check FIRST
    if contains_distress_keywords(user_query):
        response = get_safety_message()   # fixed

        try:
            log_chat(session_id, user_query, response, is_crisis=True)
        except:
            pass

        return {"response": response}

    # Normal chatbot flow
    from chat_engine import get_response
    response = get_response(session_id, user_query)

    try:
        log_chat(session_id, user_query, response, is_crisis=False)
    except:
        pass

    return {"response": response}



# uvicorn main:app --reload