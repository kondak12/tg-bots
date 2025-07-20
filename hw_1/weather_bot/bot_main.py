import asyncio, random
from aiogram import types, Bot, Dispatcher, filters, F
from aiogram.filters import CommandObject
from aiogram.utils.keyboard import ReplyKeyboardBuilder

import config


bot = Bot(token=config.TOKEN)
dispatcher = Dispatcher()
session_log = []
current_temp = None
current_temp_type = None
current_city = None


def keyboard_builder(buttons_list: list, keyboard_size: int):
    builder = ReplyKeyboardBuilder()

    for button in buttons_list:
        builder.add(types.KeyboardButton(text=str(button)))

    builder.adjust(keyboard_size)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

def get_weather(city_name):
    global current_city, current_temp, current_temp_type

    temperature_diapason = [-10, 30] if current_temp_type == config.CELSIUS else [14, 86]
    current_temp = random.randint(temperature_diapason[0], temperature_diapason[1])

    if city_name is None:
        return "Введите назание города после /weather\nПример: /weather Moscow"
    else:
        current_city = city_name.lower()
        if current_city in config.ACCESS_CITIES:
            session_log.append("take_weather_city")
            return (f"Погода в городe {current_city[0].upper() + current_city[1:]}: "
                    f"\nТемпература: {current_temp} {current_temp_type}\nОписание: ясно")
        else:
            return (f"Заданного города нет в списке доступных городов."
                    f"\n(Moscow, London, Tokyo)")


@dispatcher.message(filters.CommandStart())
async def start_dialogue(message: types.Message):

    session_log.append("/start")
    user_id = message.from_user.id

    if user_id not in config.database:
        config.database[user_id] = config.CELSIUS

    keyboard = keyboard_builder(
        [config.CELSIUS, config.FAHRENHEIT],
        2
    )
    await message.answer(
        f"Приветствую, {message.from_user.first_name}! Какую систему исчисления температуры предпочитаете?",
        reply_markup=keyboard
    )


@dispatcher.message(F.text.in_([config.CELSIUS, config.FAHRENHEIT]))
async def temp_type_choice(message: types.Message):
    global current_temp_type

    if session_log[-1] == "/start":
        session_log.append("temp_type_choice")
        if message.text == config.CELSIUS:
            config.database[message.from_user.id] = config.CELSIUS
        else:
            config.database[message.from_user.id] = config.FAHRENHEIT
        current_temp_type = config.database[message.from_user.id]

        await message.reply(f"Отлично!"
                            f"\nМожете ввести /help для показа всех команд!")

@dispatcher.message(filters.Command(config.COMMAND_HELP))
async def help_command(message: types.Message):
    await message.answer("/start - начало работы/перезагрузка бота"
                         "\n/weather <city> - вывод температуры в <city>"
                         "\n/convert - конвертация температуры ℃ -> ℉ и наоборот")

@dispatcher.message(filters.Command(config.COMMAND_WEATHER))
async def take_weather_city(message: types.Message, command: CommandObject):
    global current_city

    current_city = command.args
    weather = get_weather(current_city)
    keyboard = None

    if session_log[-1] == "take_weather_city":
        keyboard = keyboard_builder(["Обновить"], 1)

    await message.answer(weather, reply_markup=keyboard)

@dispatcher.message(F.text == config.BUTTON_UPDATE)
async def weather_update(message: types.Message):
    global current_temp, current_city

    if session_log[-1] == "take_weather_city":
        await message.answer(get_weather(current_city))
    else:
        await message.answer(f"Данную команду нужно вводить после выведенной информации о погоде, чтобы обновить её.")

@dispatcher.message(filters.Command(config.COMMAND_CONVERT))
async def temp_convert(message: types.Message):
    if session_log[-1] in ["take_weather_city"]:
        session_log.append("temp_convert")
        await message.answer(f"Конвертированная температура:"
                             f"\n{int(current_temp * 9/5 + 32 if current_temp_type == config.CELSIUS else (current_temp - 32) * 5/9)} "
                             f"{config.FAHRENHEIT if current_temp_type == config.CELSIUS else config.CELSIUS}"
                             )
    else:
        await message.answer(f"Данную команду нужно вводить после выведенной информации о погоде. "
                             f"Введите /weather <city> -> потом /convert")


async def main():
    await dispatcher.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())