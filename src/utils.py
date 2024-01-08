import os

from PIL import Image
from rembg import new_session, remove

from loggers import logger


async def remove_bg_image(input_path: str, output_path: str, user_model: str = "u2net") -> bool:
    """
    Функция удаляет фон с изображений.

    :param input_path: Путь к входному изображению
    :param output_path: Путь для сохранения обработанного изображения
    :param user_model: Название модели

    :return: True, если изображение успешно обработано и False, в случае возникновения ошибки
    """
    flag = False
    try:
        if not os.path.isfile(input_path):
            raise FileNotFoundError("Файл не найден")
        session = new_session(model_name=user_model)
        input_img = Image.open(input_path)
        output_img = remove(data=input_img, session=session)
        output_img.save(output_path)
        flag = True
        logger.error("[+] Успешно обработано изображение")
    except FileNotFoundError as val_ex:
        logger.error(f"{val_ex.__class__.__name__}: {val_ex}")
    except Exception as ex:
        logger.debug(f"{ex.__class__.__name__}: {ex}", exc_info=True)
    finally:
        return flag
