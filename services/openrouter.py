import aiohttp
import base64
from config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, GROK_MODEL, IMAGE_MODEL


async def get_completion(messages: list[dict], max_tokens: int = 1024) -> str:
    """Send messages to Grok via OpenRouter and get a response."""
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/Hemalurgic/melkior",
        "X-Title": "Melkior Discord Bot",
    }

    payload = {
        "model": GROK_MODEL,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": 0.9,
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{OPENROUTER_BASE_URL}/chat/completions",
            headers=headers,
            json=payload,
        ) as response:
            if response.status != 200:
                error_text = await response.text()
                raise Exception(f"OpenRouter API error ({response.status}): {error_text}")

            data = await response.json()
            return data["choices"][0]["message"]["content"]


async def generate_image(prompt: str) -> bytes:
    """Generate an image via OpenRouter and return image bytes."""
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/Hemalurgic/melkior",
        "X-Title": "Melkior Discord Bot",
    }

    payload = {
        "model": IMAGE_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "modalities": ["image", "text"],
        "provider": {
            "order": ["google-ai-studio"],
            "allow_fallbacks": False
        },
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{OPENROUTER_BASE_URL}/chat/completions",
            headers=headers,
            json=payload,
        ) as response:
            if response.status != 200:
                error_text = await response.text()
                raise Exception(f"OpenRouter image API error ({response.status}): {error_text}")

            data = await response.json()
            message = data["choices"][0]["message"]

            # Extract base64 image from response
            if "images" in message and message["images"]:
                image_url = message["images"][0]["image_url"]["url"]
                # Remove data URL prefix if present
                if image_url.startswith("data:"):
                    image_url = image_url.split(",", 1)[1]
                return base64.b64decode(image_url)

            raise Exception("No image in response")
