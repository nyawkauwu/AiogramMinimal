import asyncio

from dotenv import load_dotenv
from os import environ
load_dotenv()

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

TOKEN = environ.get("BOT_TOKEN")

bot: Bot
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(msg: Message):
    await msg.answer(f"Hello, {html.quote(msg.from_user.full_name)}!")


@dp.message(Command("help"))
async def command_start_handler(msg: Message):
    await msg.answer(f"Sorry, I can't help you.")


@dp.message()
async def message_handler(msg: Message):
    await msg.answer("Meow!")


async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())