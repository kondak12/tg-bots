import aiogram, asyncio

from handlers import add_book, list_books, mark_read, remove_book, start
from config import TOKEN, BOOK_REPOSITORY


async def main():
    bot = aiogram.Bot(token=TOKEN)
    dp = aiogram.Dispatcher()
    dp.include_routers(
        add_book.router,
        list_books.router,
        mark_read.router,
        remove_book.router,
        start.router
    )

    await BOOK_REPOSITORY.init_tables()

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())