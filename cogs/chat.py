import random
import discord
from discord.ext import commands

from config import INTERJECTION_CHANCE
from prompts.melkior import SYSTEM_PROMPT, INTERJECTION_PROMPT
from services.openrouter import get_completion
from services.database import save_message, get_conversation_history


class Chat(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # Ignore messages from bots (including self)
        if message.author.bot:
            return

        # Check if bot was mentioned
        bot_mentioned = self.bot.user in message.mentions

        if bot_mentioned:
            await self.handle_mention(message)
        elif random.random() < INTERJECTION_CHANCE:
            await self.handle_interjection(message)

    async def handle_mention(self, message: discord.Message):
        """Respond when directly mentioned."""
        async with message.channel.typing():
            # Clean the message content (remove the mention)
            content = message.content
            for mention in message.mentions:
                content = content.replace(f"<@{mention.id}>", "").replace(f"<@!{mention.id}>", "")
            content = content.strip()

            if not content:
                content = "Someone summons me without purpose..."

            # Get conversation history and format as context
            history = await get_conversation_history(str(message.channel.id))

            # Build system prompt with memory as context (not conversation turns)
            system_with_memory = SYSTEM_PROMPT
            if history:
                memory_lines = []
                for msg in history[-10:]:  # Last 10 messages max
                    memory_lines.append(msg["content"])
                system_with_memory += "\n\nRECENT MEMORY (for context only, do not re-answer):\n" + "\n".join(memory_lines)

            # Build messages - only ONE user message
            messages = [
                {"role": "system", "content": system_with_memory},
                {"role": "user", "content": f"[{message.author.display_name}]: {content}"}
            ]

            try:
                response = await get_completion(messages)

                # Save to database
                await save_message(
                    str(message.author.id),
                    str(message.channel.id),
                    "user",
                    f"[{message.author.display_name}]: {content}"
                )
                await save_message(
                    str(self.bot.user.id),
                    str(message.channel.id),
                    "assistant",
                    response
                )

                # Send response (split if too long)
                await self.send_long_message(message.channel, response)

            except Exception as e:
                await message.channel.send(
                    f"*Melkior's crystal ball flickers and dims...* (Error: {str(e)[:100]})"
                )

    async def handle_interjection(self, message: discord.Message):
        """Randomly interject with a grumpy comment."""
        async with message.channel.typing():
            messages = [
                {"role": "system", "content": INTERJECTION_PROMPT},
                {"role": "user", "content": f"[Overheard in the tavern] {message.author.display_name}: {message.content}"}
            ]

            try:
                response = await get_completion(messages, max_tokens=150)
                await message.channel.send(f"*mutters from the corner*\n{response}")
            except Exception:
                pass  # Silently fail for interjections

    async def send_long_message(self, channel: discord.TextChannel, content: str):
        """Send a message, splitting if it exceeds Discord's limit."""
        if len(content) <= 2000:
            await channel.send(content)
        else:
            # Split by paragraphs first, then by length
            chunks = []
            current_chunk = ""
            for paragraph in content.split("\n\n"):
                if len(current_chunk) + len(paragraph) + 2 > 1900:
                    if current_chunk:
                        chunks.append(current_chunk)
                    current_chunk = paragraph
                else:
                    current_chunk = current_chunk + "\n\n" + paragraph if current_chunk else paragraph
            if current_chunk:
                chunks.append(current_chunk)

            for chunk in chunks:
                await channel.send(chunk)


async def setup(bot: commands.Bot):
    await bot.add_cog(Chat(bot))
