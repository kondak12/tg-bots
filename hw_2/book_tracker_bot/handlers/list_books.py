from aiogram.filters import command
from aiogram import types, Router
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from hw_2.book_tracker_bot.config import BOOK_SERVICE


router = Router()

@router.message(command.Command("list_books"))
async def list_books_handler(message: types.Message):
    user_id = message.from_user.id
    books = await BOOK_SERVICE.list_books(user_id)

    if not books:
        await message.answer("Ваш список книг пуст.")
        return

    kb_builder = InlineKeyboardBuilder()
    for book in books:
        kb_builder.row(
            InlineKeyboardButton(
                text=f"Удалить {book.title}",
                callback_data=f"remove_{book.id}"
            )
        )

    book_list = "\n".join(
        f"{book.id}: {book.title} ({book.pages_read}/{book.pages_count})"
        for book in books
    )
    await message.answer(
        f"Ваши книги:\n{book_list}",
        reply_markup=kb_builder.as_markup()
    )