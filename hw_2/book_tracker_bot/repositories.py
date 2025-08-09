import aiosqlite

from models import Book


class BookRepository:

    def __init__(self, db_path: str) -> None:
        self.db_path = db_path

    async def init_tables(self) -> None:
        sql_command = """
        CREATE TABLE IF NOT EXISTS `Books` (
            `id` INTEGER PRIMARY KEY AUTOINCREMENT,
            `user_id` INTEGER NOT NULL,
            `title` TEXT NOT NULL,
            `pages_read` INTEGER DEFAULT 0,
            `pages_count` INTEGER NOT NULL,
            `created_at` TEXT DEFAULT CURRENT_TIMESTAMP
        );
    """
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(sql_command)
            await db.commit()

    async def create_book(self, user_id: int, title: str, pages_count: int) -> Book:
        sql_command = """
        INSERT INTO `Books` (`user_id`, `title`, `pages_count`) VALUES (
            ?, ?, ?
        );
    """
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row

            await db.execute(sql_command, [user_id, title, pages_count])
            await db.commit()

            cursor = await db.execute("""
            SELECT * FROM `Books` 
                WHERE `title` = ?;
            """, [title]
        )
            # row_book = {'user_id': 1, 'id': 1, ...}
            row_book = await cursor.fetchone()
            return Book(**dict(row_book))

    async def update_pages(self, user_id, book_id: int, pages: int) -> Book:
        sql_command = """
        UPDATE TABLE `Books` SET `pages_read` = ?
            WHERE `id` = ? AND `user_id` = ?;
        """

        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row

            await db.execute(sql_command, [pages, book_id, user_id])
            await db.commit()

            cursor = await db.execute( """
            SELECT * FROM `Books` 
                WHERE `id` = ?;
            """, [book_id]
        )
            row_book = await cursor.fetchone()
            return Book(**dict(row_book))

    async def fetch_books(self, user_id: int):
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row

            cursor = await db.execute("""
                SELECT * FROM `Books` 
                    WHERE `user_id` = ?;
            """, [user_id]
            )

            return [
                Book(**dict(row_book))
                for row_book in await cursor.fetchall()
            ]

    async def get_pages_read(self, user_id):
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row

            cursor = await db.execute("""
                SELECT `pages_read` FROM `Books` 
                    WHERE `user_id` = ?;
            """, [user_id]
            )

            row_book = await cursor.fetchone()
            return Book(**dict(row_book)).pages_read

    async def delete_book(self, user_id: int, book_id: int) -> None:
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row

            await db.execute( """
            DELETE FROM `Books`
                WHERE `id` = ? AND `user_id` = ?;
            """, [book_id, user_id]
            )
            await db.commit()