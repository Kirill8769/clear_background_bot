import os

PATH_PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LIST_OF_EXTENSIONS = [".jpg", ".jpeg", ".png"]

INFO_MESSAGE = """
Я могу обрабатывать изображения в нескольких режимах:
Стандартный режим: Удаляет простой однородный фон, такой как белые стены или голубое небо.
Улучшенный режим: Подходит для более сложных фонов с текстурами или узорами.
Обработка человека: Модель для сегментации человека
Обработка одежды: Модель для разбора ткани по фото человека
Обработка аниме: Высокоточная сегментация персонажей аниме.
"""

START_MESSAGE = """
Привет человек!

Я телеграм-бот, создан для того чтобы помогать людям удалять задний фон с изображений.
Подробнее о моих возможностях можно узнать нажав на кнопку "Информация о боте"
"""

MODELS = [
    "u2net:Стандартная обработка (по-умолчанию)",
    "isnet-general-use:Улучшенная обработка",
    "u2net_human_seg:Обработка человека",
    "u2net_cloth_seg:Обработка одежды",
    "isnet-anime:Обработка аниме"
]