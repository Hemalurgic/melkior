import aiohttp
from config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, GROK_MODEL


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
