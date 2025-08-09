from models import Book, UserStats
from repositories import BookRepository

"""
CREATE TABLE Persons (
    name VARCHAR(128),
    age INTEGER
);
"""

"""
USE database;

UPDATE `Persons` SET `name` = 'Дмитрий'
    WHERE `age` > 22;

INSERT INTO `Persons` VALUES
    ('Shaban', 17),
    ('Ivan', 20);
    
DELETE FROM `Persons`
    WHERE (`Persons`.`age` = 18 OR `Persons`.`name` = 'Шабан');

"""

class BookService:

    def __init__(self, book_repo: BookRepository):
        self._repo = book_repo

    async def add_book(self, user_id: int, book: Book) -> Book:
        return await self._repo.create_book(user_id, book.title, book.pages_count)

    async def increase_read_pages(self, user_id: int, book_id: int, pages: int) -> Book:
        return await self._repo.update_pages(user_id, book_id, pages)

    async def list_books(self, user_id: int) -> list[Book]:
        return await self._repo.fetch_books(user_id)

    async def remove_book(self, user_id: int, book_id: int) -> None:
        return await self._repo.delete_book(user_id, book_id)


class StatsService:
    def __init__(self, book_repo):
        self._repo = book_repo

    async def get_stats(self, user_id: int) -> UserStats:
        return UserStats(
            user_id,
            self._repo.fetch_books(user_id),
            self._repo.get_pages_read(user_id)
        )