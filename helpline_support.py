from typing import List
import random

# Distress keywords
DISTRESS_KEYWORDS: List[str] = [
    "suicidal", "suicide", "kill myself", "want to die",
    "hopeless", "worthless", "can't go on", "give up",
    "ending it all", "no reason to live", "tired of life",
    "feel empty", "no point in living", "better off dead",
    "hurt myself", "self harm", "alone and broken",
    "end my life", "i don't want to live", "life is meaningless",
    "i feel like dying"
]

# Full message (kept for reference/logging if needed)
SAFETY_MESSAGE = (
    "It sounds like you're going through a really difficult moment.\n\n"
    "You are not alone, even if it feels that way right now.\n"
    "There are people who genuinely care about you and want to support you.\n\n"
    "If you can, please consider talking to someone you trust.\n\n"
    "Here are some helplines you can contact:\n\n"
    "India:\n"
    "9152987821 (iCall)\n"
    "1800-599-0019 (Vandrevala Foundation)\n"
)

# Short, empathetic responses (randomized)
SAFETY_MESSAGES = [
    (
        "I’m really sorry you’re feeling this way. It sounds like a lot to carry, "
        "and I’m really glad you reached out.\n\n"
        "You’re not alone in this, even if it feels that way right now. "
        "There are people who genuinely care and want to support you.\n\n"
        "You can talk to someone right now: 9152987821 (iCall)\n\n"
        "If you’d like to share more or just talk, I’m here to listen."
    ),
    (
        "That sounds really overwhelming, and I’m really glad you spoke up. "
        "It takes strength to say how you’re feeling.\n\n"
        "Even if things feel heavy right now, you don’t have to go through it alone. "
        "There is support available for you.\n\n"
        "You can reach out here: 9152987821 (iCall)\n\n"
        "If you feel like talking more about it, I’m here with you."
    ),
    (
        "I’m really sorry you’re going through this. It sounds exhausting and difficult, "
        "and I’m really glad you reached out.\n\n"
        "You deserve support and care during moments like this. "
        "There are people who are ready to listen and help.\n\n"
        "Try calling: 9152987821 (iCall)\n\n"
        "If you want to share what’s been on your mind, I’m here for you."
    )
]

# Keyword detection
def contains_distress_keywords(text: str) -> bool:
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in DISTRESS_KEYWORDS)

# Get short response
def get_safety_message() -> str:
    return random.choice(SAFETY_MESSAGES)