from service import BookService, BookRepository


TOKEN = "TOKEN"

BOOK_REPOSITORY = BookRepository("database.db")
BOOK_SERVICE = BookService(BOOK_REPOSITORY)