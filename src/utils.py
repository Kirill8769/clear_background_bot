import os

from rembg import new_session, remove
from PIL import Image

from config import PATH_PROJECT, LIST_OF_EXTENSIONS
from loggers import logger


async def remove_bg_images(input_path: str, output_path: str, user_model: str = "u2net"):
    """
    FUNC INFO
    """

    try:
        if not os.path.isfile(input_path):
            raise ValueError("Файл не найден")

        session = new_session(model_name=user_model)
        input_img = Image.open(input_path)
        output_img = remove(data=input_img, session=session)
        output_img.save(output_path)

        # for file in os.listdir(input_path):
        #     file_format = f".{file.split('.')[-1]}"
        #     if file_format in LIST_OF_EXTENSIONS:
        #         file_name = file.split(".")[0]
        #         input_path_image = os.path.join(input_path, file)
        #         outpup_path_image = os.path.join(outpup_path, f"out2_{file_name}.png")
        #         input_img = Image.open(input_path_image)
        #         output_img = remove(data=input_img, session=session)
        #         output_img.save(outpup_path_image)
    except ValueError as val_ex:
        logger.error(f"{val_ex.__class__.__name__}: {val_ex}")
    except Exception as ex:
        logger.debug(f"{ex.__class__.__name__}: {ex}", exc_info=True)
