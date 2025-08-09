from aiogram.filters import command
from aiogram import types, Router
from aiogram.exceptions import AiogramError

from hw_2.book_tracker_bot.config import BOOK_SERVICE


router = Router()

@router.message(command.Command("add_book"))
async def add_book_handler(message: types.Message, command: command.CommandObject):
    if not command.args:
        await message.answer("Использование: /add_book <название> <количество страниц>")
        return

    try:
        args = command.args.split()
        if len(args) < 2:
            raise ValueError

        title = " ".join(args[:-1])
        pages_count = int(args[-1])
        user_id = message.from_user.id

        await BOOK_SERVICE.add_book(user_id, title, pages_count)
        await message.answer(f"Книга '{title}' добавлена!")

    except ValueError:
        await message.answer("Один из параметров введён неверно.\n"
                             "Используйте: /add_book <название> <количество страниц>")
    except AiogramError:
        await message.answer(f"Ошибка при добавлении книги.")