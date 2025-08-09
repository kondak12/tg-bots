from aiogram.filters import command
from aiogram import Router, types
from aiogram.exceptions import AiogramError

from hw_2.book_tracker_bot.config import BOOK_SERVICE


router = Router()

@router.message(command.Command("mark_read"))
async def mark_read_handler(message: types.Message, command: command.CommandObject):
    if not command.args:
        await message.answer("Использование: /mark_read <id книги> <прочитано страниц>")
        return

    try:
        args = command.args.split()
        if len(args) != 2:
            raise ValueError

        book_id = int(args[0])
        pages = int(args[1])
        user_id = message.from_user.id

        await BOOK_SERVICE.increase_read_pages(user_id, book_id, pages)
        await message.answer(f"Прогресс обновлен!")

    except (ValueError, IndexError):
        await message.answer("Один из параметров введён неверно.\n"
                             "Используйте: /mark_read <id книги> <прочитано страниц>")

    except AiogramError:
        await message.answer(f"Ошибка при обновлении")