from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from config import MODELS


async def get_keyboard_start():
    markup = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Информация о боте")],
        [KeyboardButton(text="Настройка обработчика")]],
        resize_keyboard=True, selective=True)
    return markup


async def get_keyboard_settings(user_model):
    buttons = []
    for button in MODELS:
        if user_model == button.split(":")[0]:
            buttons.append([KeyboardButton(text=f"✅{button.split(':')[-1]}")])
        else:
            buttons.append([KeyboardButton(text=button.split(':')[-1])])
    buttons.append([KeyboardButton(text="На главную")])
    markup = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, selective=True)
    return markup
