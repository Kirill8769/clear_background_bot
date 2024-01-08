import os
from random import randint

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart, Filter

from config import INFO_MESSAGE, MODELS, PATH_PROJECT, START_MESSAGE
from db import RemDb
from keyboards import get_keyboard_settings, get_keyboard_start
from utils import remove_bg_image

dp = Dispatcher()
rem_db = RemDb()


class MyFilter(Filter):
    async def __call__(self, message: types.Message) -> bool:
        """
        Фильтр для проверки, содержится ли текст сообщения в последних частях строк моделей.

        :param message: Объект сообщения от пользователя.
        :return: True, если текст сообщения содержится в конечных частях строк моделей, иначе False.
        """
        return message.text in [model.split(":")[-1] for model in MODELS]


@dp.message(CommandStart())
async def command_start(message: types.Message) -> None:
    """
    Обработчик команды /start.

    :param message: Объект сообщения от пользователя.
    """
    if not message.from_user.is_bot:
        await message.answer(START_MESSAGE, parse_mode="HTML", reply_markup=await get_keyboard_start())
        await rem_db.new_user(message.from_user)


@dp.message(F.text == "Информация о боте")
async def get_bot_info(message: types.Message) -> None:
    """
    Обработчик сообщения с текстом "Информация о боте".

    :param message: Объект сообщения от пользователя.
    """
    await rem_db.get_model(str(message.from_user.id))
    await message.answer(text=INFO_MESSAGE, parse_mode="HTML")


@dp.message(F.text == "Выбрать режим обработки")
async def get_settings(message: types.Message) -> None:
    """
    Обработчик сообщения с текстом "Выбрать режим обработки".

    :param message: Объект сообщения от пользователя.
    """
    user_model = await rem_db.get_model(str(message.from_user.id))
    await message.answer(text="Выберите режим", reply_markup=await get_keyboard_settings(user_model))


@dp.message(MyFilter())
async def button_handlers(message: types.Message) -> None:
    """
    Обработчик сообщений, проходящих через фильтр MyFilter.

    :param message: Объект сообщения от пользователя.
    """
    user_id = str(message.from_user.id)
    for model in MODELS:
        if message.text in model:
            check_model = model.split(":")[0]
            check_model_name = model.split(":")[-1]
            break
    await rem_db.set_model(user_id, check_model)
    await message.answer(text=f"Установлен режим: {check_model_name}", reply_markup=await get_keyboard_start())


@dp.message(F.text == "На главную")
async def return_on_main_page(message: types.Message) -> None:
    """
    Обработчик сообщения с текстом "На главную".

    :param message: Объект сообщения от пользователя.
    """
    await message.answer(text="Главная", reply_markup=await get_keyboard_start())


@dp.message(F.photo)
async def get_image(message: types.Message, bot: Bot) -> None:
    """
    Обработчик сообщений с изображениями (фотографиями).

    :param message: Объект сообщения от пользователя с изображением.
    :param bot: Объект бота для взаимодействия с Telegram API.
    """
    await message.answer("Обрабатываю ...")
    user_id = str(message.from_user.id)
    random_name = randint(1, 9999999)
    user_model = await rem_db.get_model(user_id=user_id)
    input_path = os.path.join(PATH_PROJECT, "input_imgs", f"{user_id}_{random_name}.png")
    output_path = os.path.join(PATH_PROJECT, "output_imgs", f"out_{user_id}_{random_name}.png")
    img = await bot.get_file(message.photo[-1].file_id)
    await bot.download_file(img.file_path, input_path)
    await remove_bg_image(input_path=input_path, output_path=output_path, user_model=user_model)
    if os.path.isfile(output_path):
        out_img = types.FSInputFile(output_path)
        await bot.send_document(message.from_user.id, document=out_img)
        os.remove(output_path)
    else:
        await message.answer(text="Произошла ошибка при обработке файла, повторите попытку")
    os.remove(input_path)


@dp.message()
async def other_message(message: types.Message) -> None:
    """
    Обработчик прочих сообщений.

    :param message: Объект сообщения от пользователя.
    """
    await message.delete()
