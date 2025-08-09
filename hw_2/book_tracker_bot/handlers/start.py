from aiogram.filters import command
from aiogram import types, Router


router = Router()

@router.message(command.CommandStart())
async def start_handler(message: types.Message):
    await message.answer("Данный бот предназначен для работы с книжной библиотекой.\n\n"
                         "Основные команды:\n"
                         " - /start Регистрация нового пользователя и инициализация БД\n"
                         " - /add_book <название> Добавить книгу с указанным названием\n"
                         " - /mark_read <id> <pages> Добавить к книге с ID равным <id> число прочитанных страниц\n"
                         " - /list_books Показать список всех книг с их ID и прогрессом\n"
                         " - /remove_book <id> Удалить книгу с указанным ID\n"
                         " - /stats Показать общее количество книг и общее число прочитанных страниц")