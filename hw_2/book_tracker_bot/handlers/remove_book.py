from aiogram.filters import command
from aiogram import Router, F, types
from aiogram.exceptions import AiogramError

from hw_2.book_tracker_bot.config import BOOK_SERVICE


router = Router()

@router.message(command.Command("remove_book"))
async def remove_handler(message: types.Message, command: command.CommandObject):
    if not command.args:
        await message.answer("Использование: /remove_book <id книги>")
        return

    try:
        book_id = int(command.args)
        user_id = message.from_user.id
        await BOOK_SERVICE.remove_book(user_id, book_id)
        await message.answer(f"Книга {book_id} удалена!")

    except ValueError:
        await message.answer("Неверный id. Используйте: /remove_book <id книги>")

    except AiogramError:
        await message.answer(f"Ошибка при удалении")

@router.callback_query(F.data.startswith("remove_"))
async def remove_callback_handler(callback: types.CallbackQuery):
    try:
        book_id = int(callback.data.split("_")[1])
        user_id = callback.from_user.id
        await BOOK_SERVICE.remove_book(user_id, book_id)
        await callback.message.answer(f"Книга {book_id} удалена!")

    except (ValueError, IndexError, AiogramError):
        await callback.message.answer(f"Ошибка при удалении.")

    await callback.answer()