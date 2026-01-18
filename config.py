import os
from dotenv import load_dotenv

load_dotenv()

# Discord
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN environment variable is required")

# OpenRouter
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY environment variable is required")

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
GROK_MODEL = "x-ai/grok-4.1-fast"

# Bot behavior
INTERJECTION_CHANCE = float(os.getenv("INTERJECTION_CHANCE", "0.05"))
MAX_CONVERSATION_HISTORY = 20  # Messages to remember per channel

# Image generation
IMAGE_MODEL = "google/gemini-2.5-flash-image-preview"
IMAGE_TRIGGERS = ["draw", "paint", "sketch", "conjure", "show me", "picture of", "image of", "illustrate", "visualize"]
