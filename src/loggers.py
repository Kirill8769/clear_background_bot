import logging.config
import os
from datetime import datetime

from config import PATH_PROJECT


def my_logger() -> logging.Logger:
    """
    Функция для настройки и получения экземпляра логгера.

    :return: Объект логгера с настроенным файловым обработчиком.
    """
    try:
        file_logger = logging.getLogger("logger")
        file_logger.setLevel("DEBUG")
        log_file = os.path.join(PATH_PROJECT, "logs", f'log_{datetime.today().strftime("%d_%m_%Y")}.log')
        file_handler = logging.FileHandler(filename=log_file, encoding="UTF-8")
        file_formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s %(filename)s-%(funcName)s: %(message)s", datefmt="%d.%m.%Y-%H:%M:%S"
        )
        file_handler.setFormatter(file_formatter)
        file_logger.addHandler(file_handler)
        return file_logger
    except Exception as ex:
        ex_logger = logging.getLogger()
        ex_logger.debug(f"{ex.__class__.__name__}: {ex}", exc_info=True)
        return ex_logger


logger = my_logger()
