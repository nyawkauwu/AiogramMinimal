import asyncio

from dotenv import load_dotenv
from os import environ
load_dotenv()

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from asyncpg import Pool, create_pool

TOKEN = environ.get("BOT_TOKEN")

bot: Bot
pool: Pool
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(msg: Message):
    async with pool.acquire() as connection:
        async with connection.transaction():
            cursor = await connection.cursor("SELECT tg_id FROM users WHERE tg_id = $1", msg.from_user.id)
            db_user = await cursor.fetchrow()
            if not db_user:
                await connection.execute("INSERT INTO users (tg_id, username, first_name) VALUES ($1, $2, $3)",
                    msg.from_user.id, msg.from_user.username, msg.from_user.first_name)
    await msg.answer(f"Hello, {html.quote(msg.from_user.full_name)}!")


@dp.message(Command("help"))
async def command_start_handler(msg: Message):
    await msg.answer(f"Sorry, I can't help you.")


@dp.message()
async def message_handler(msg: Message):
    await msg.answer("Meow!")


async def main():
    global pool
    pool = await create_pool(environ["PSQL_URI"], min_size=1, max_size=10, max_inactive_connection_lifetime=0)
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())