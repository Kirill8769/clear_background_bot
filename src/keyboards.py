from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from config import MODELS


async def get_keyboard_start() -> ReplyKeyboardMarkup:
    """
    Функция для получения клавиатуры стартового меню.

    :return: Объект ReplyKeyboardMarkup, представляющий клавиатуру.
    """
    markup = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Информация о боте")], [KeyboardButton(text="Выбрать режим обработки")]],
        resize_keyboard=True,
        selective=True,
    )
    return markup


async def get_keyboard_settings(user_model: str) -> ReplyKeyboardMarkup:
    """
    Функция для получения клавиатуры настроек пользователя.

    :param user_model: Модель, выбранная пользователем.
    :return: Объект ReplyKeyboardMarkup, представляющий клавиатуру настроек.
    """
    buttons = []
    for button in MODELS:
        if user_model == button.split(":")[0]:
            buttons.append([KeyboardButton(text=f"✅{button.split(':')[-1]}")])
        else:
            buttons.append([KeyboardButton(text=button.split(":")[-1])])
    buttons.append([KeyboardButton(text="На главную")])
    markup = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, selective=True)
    return markup
