import aiosqlite
from pathlib import Path
from config import MAX_CONVERSATION_HISTORY

DB_PATH = Path(__file__).parent.parent / "melkior.db"


async def init_db():
    """Initialize the database and create tables if they don't exist."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY,
                user_id TEXT NOT NULL,
                channel_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.execute("""
            CREATE INDEX IF NOT EXISTS idx_channel ON conversations(channel_id)
        """)
        await db.commit()


async def save_message(user_id: str, channel_id: str, role: str, content: str):
    """Save a message to the conversation history."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO conversations (user_id, channel_id, role, content) VALUES (?, ?, ?, ?)",
            (user_id, channel_id, role, content),
        )
        await db.commit()


async def get_conversation_history(channel_id: str) -> list[dict]:
    """Get recent conversation history for a channel."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            """
            SELECT role, content FROM conversations
            WHERE channel_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
            """,
            (channel_id, MAX_CONVERSATION_HISTORY),
        )
        rows = await cursor.fetchall()

    # Reverse to get chronological order
    messages = [{"role": row["role"], "content": row["content"]} for row in reversed(rows)]
    return messages


async def clear_channel_history(channel_id: str):
    """Clear conversation history for a channel."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM conversations WHERE channel_id = ?", (channel_id,))
        await db.commit()
