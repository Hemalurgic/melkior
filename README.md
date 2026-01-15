# Melkior

A cantankerous wizard Discord bot for D&D 5e, powered by Grok via OpenRouter.

Melkior is an ancient, grumpy wizard who serves as an unwilling advisor to adventurers. He speaks in riddles and archaic language, but his cryptic answers contain real, actionable D&D 5e advice.

## Features

- **D&D 5e Expert**: Rules, builds, strategy - all wrapped in cryptic wizard-speak
- **Persistent Memory**: Remembers conversations and can hold grudges
- **Random Interjections**: Occasionally grumbles about what's being said
- **In-Character Always**: Never breaks the fourth wall

## Setup

### 1. Create a Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application named "Melkior"
3. Go to "Bot" section and create a bot
4. Enable these Privileged Gateway Intents:
   - Message Content Intent
5. Copy the bot token

### 2. Get OpenRouter API Key

1. Go to [OpenRouter](https://openrouter.ai/)
2. Create an account and get an API key

### 3. Install & Configure

```bash
# Clone the repository
git clone https://github.com/Hemalurgic/melkior.git
cd melkior

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Configure environment
copy .env.example .env  # Windows
# cp .env.example .env  # Linux/Mac

# Edit .env with your tokens
```

### 4. Invite Bot to Server

1. Go to Discord Developer Portal > Your App > OAuth2 > URL Generator
2. Select scopes: `bot`
3. Select permissions: `Send Messages`, `Read Message History`
4. Copy the generated URL and open it to invite Melkior

### 5. Run

```bash
python bot.py
```

## Usage

- **Mention Melkior**: `@Melkior what's the best way to build a paladin?`
- Melkior will respond in character with cryptic but useful advice
- He remembers your conversation history per channel
- Occasionally, he'll interject with grumpy comments

## Configuration

Edit `.env` to customize:

| Variable | Description | Default |
|----------|-------------|---------|
| `DISCORD_TOKEN` | Your Discord bot token | Required |
| `OPENROUTER_API_KEY` | Your OpenRouter API key | Required |
| `INTERJECTION_CHANCE` | Chance to randomly comment (0.0-1.0) | 0.05 |

## License

MIT
