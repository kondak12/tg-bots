from models import Book, UserStats
from repositories import BookRepository


class BookService:

    def __init__(self, book_repo: BookRepository):
        self._repo = book_repo

    async def add_book(self, user_id: int, title: str, pages_count: int) -> Book:
        return await self._repo.create_book(user_id, title, pages_count)

    async def increase_read_pages(self, user_id: int, book_id: int, pages: int) -> Book:
        return await self._repo.update_pages(user_id, book_id, pages)

    async def list_books(self, user_id: int) -> list[Book]:
        return await self._repo.fetch_books(user_id)

    async def remove_book(self, user_id: int, book_id: int) -> None:
        return await self._repo.delete_book(user_id, book_id)


class StatsService:
    def __init__(self, book_repo: BookRepository):
        self._repo = book_repo

    async def get_stats(self, user_id: int) -> UserStats:
        books = await self._repo.fetch_books(user_id)
        total_pages = sum(book.pages_read for book in books)

        return UserStats(
            user_id,
            len(books),
            total_pages
        )