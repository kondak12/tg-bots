import asyncio

from repositories import BookRepository


async def main():

    book_repo = BookRepository("database.db")
    await book_repo.init_tables()

    print(await book_repo.fetch_books(user_id=1))

    await book_repo.delete_book(user_id=1, book_id=1)

    print(await book_repo.fetch_books(user_id=1))


if __name__ == "__main__":
    asyncio.run(main())