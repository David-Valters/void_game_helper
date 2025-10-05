from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("TOKEN_BOT")

if not TOKEN:
    raise ValueError("TOKEN_BOT is not set in environment variables")

bot = Bot(TOKEN)
dp = Dispatcher()

@dp.message()
async def get_chat_id(message: Message):
    # await message.answer(f"Chat ID: {message.chat.id}")
    print(f"Chat ID: {message.chat}")

async def main():
    await dp.start_polling(bot)

asyncio.run(main())
