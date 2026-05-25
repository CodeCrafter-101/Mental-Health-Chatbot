import os
import random
from dotenv import load_dotenv
from groq import Groq

# Load env
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Session memory
session_memory = {}

# Load docs
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data")

documents = {}

# Chunking function
def split_into_chunks(text, chunk_size=200):
    sentences = text.split(". ")
    chunks = []
    current = ""

    for s in sentences:
        if len(current) + len(s) < chunk_size:
            current += s + ". "
        else:
            chunks.append(current.strip())
            current = s + ". "

    if current:
        chunks.append(current.strip())

    return chunks


# Load and chunk documents
for file in os.listdir(DATA_PATH):
    if file.endswith(".txt"):
        with open(os.path.join(DATA_PATH, file), "r", encoding="utf-8") as f:
            documents[file] = split_into_chunks(f.read())

print("Docs Loaded (chunked):", list(documents.keys()))


# Topic detection (multi-topic)
def detect_topic(query):
    q = query.lower()
    results = []

    if "anxiety" in q:
        results += documents.get("anxiety_help.txt", [])
    if "stress" in q:
        results += documents.get("stress_management.txt", [])
    if any(word in q for word in ["lonely", "alone", "isolated"]):
        results += documents.get("loneliness.txt", [])
    if "overthink" in q:
        results += documents.get("overthinking.txt", [])
    if "motivation" in q:
        results += documents.get("motivation.txt", [])

    return results


# Best chunk selection
def get_best_chunk(chunks, query):
    query_words = set(query.lower().split())
    best_chunk = ""
    best_score = 0

    for chunk in chunks:
        chunk_words = set(chunk.lower().split())
        score = len(query_words & chunk_words)

        if score > best_score:
            best_score = score
            best_chunk = chunk

    return best_chunk


# Main function
def get_response(session_id, user_query):
    print("Query:", user_query)

    if session_id not in session_memory:
        session_memory[session_id] = []

    memory = session_memory[session_id]

    # Get chunks
    chunks = detect_topic(user_query)

    # Smart + slight randomness
    if chunks:
        best = get_best_chunk(chunks, user_query)
        context = random.choice([best] + chunks[:2])
    else:
        context = ""

    # Conversation history
    history = ""
    for chat in memory[-10:]:
        history += f"User: {chat['user']}\nBot: {chat['bot']}\n"

    # Prompt
    prompt = f"""
You are a supportive mental health assistant.

Conversation (IMPORTANT: use this to maintain context and refer to past messages):
{history}

User:
{user_query}

Context (reference only, DO NOT copy):
{context}

Instructions:
- Be empathetic
- Do NOT copy or reuse phrases from context
- Give only 1-2 helpful suggestions
- Keep it short (3-5 lines)
- Avoid repeating previous advice
- Respond slightly differently even for similar inputs

Answer:
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,   # increased for variation
        )

        answer = response.choices[0].message.content

        # Save memory
        memory.append({"user": user_query, "bot": answer})

        print("🤖", answer)

        return answer

    except Exception as e:
        print("ERROR:", str(e))
        return "Error: " + str(e)