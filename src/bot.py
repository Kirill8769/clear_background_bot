import os
from random import randint

from aiogram import Dispatcher, types, F, Bot
from aiogram.filters import CommandStart, Filter
from dotenv import load_dotenv

from config import INFO_MESSAGE, MODELS, START_MESSAGE, PATH_PROJECT
from db import RemDb
from loggers import logger
from keyboards import get_keyboard_start, get_keyboard_settings
from utils import remove_bg_images


dp = Dispatcher()
rem_db = RemDb()


async def start_db():
    await rem_db.create_table()


class MyFilter(Filter):
    async def __call__(self, message: types.Message) -> bool:
        return message.text in [model.split(":")[-1] for model in MODELS]


@dp.message(CommandStart())
async def command_start(message: types.Message):
    if not message.from_user.is_bot:
        await message.answer(START_MESSAGE, reply_markup=await get_keyboard_start())
        await rem_db.new_user(message.from_user)


@dp.message(F.text == "Информация о боте")
async def return_on_main_page(message: types.Message):
    await rem_db.get_model(str(message.from_user.id))
    await message.answer(text=INFO_MESSAGE)


@dp.message(F.text == "Настройка обработчика")
async def return_on_main_page(message: types.Message):
    user_model = await rem_db.get_model(str(message.from_user.id))
    await message.answer(text="Выберите режим", reply_markup=await get_keyboard_settings(user_model))


@dp.message(MyFilter())
async def button_handlers(message: types.Message):
    user_id = str(message.from_user.id)
    user_model = await rem_db.get_model(user_id)
    for model in MODELS:
        if message.text in model:
            check_model = model.split(":")[-1]
    await rem_db.set_model(user_id, check_model)
    await message.answer(text=f"Установлен режим: {check_model}", reply_markup=await get_keyboard_start())


@dp.message(F.text == "На главную")
async def return_on_main_page(message: types.Message):
    await message.answer(text="Главная", reply_markup=await get_keyboard_start())


@dp.message(F.photo)
async def get_image(message: types.Message, bot: Bot):
    await message.answer("Обрабатываю ...")
    user_id = str(message.from_user.id)
    random_name = randint(1, 9999999)
    input_path = os.path.join(PATH_PROJECT, "input_imgs", f"{user_id}_{random_name}.png")
    output_path = os.path.join(PATH_PROJECT, "output_imgs", f"out_{user_id}_{random_name}.png")
    img = await bot.get_file(message.photo[-1].file_id)
    await bot.download_file(img.file_path, input_path)
    await remove_bg_images(input_path=input_path, output_path=output_path)
    out_img = types.FSInputFile(output_path)
    await bot.send_document(message.from_user.id, document=out_img)
    os.remove(input_path)
    os.remove(output_path)


@dp.message()
async def other_message(message: types.Message):
    await message.delete()
