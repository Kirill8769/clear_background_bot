import asyncio
import os

import asyncpg
from dotenv import load_dotenv

from loggers import logger


class RemDb:
    """
    Класс для работы с базой данных.
    """

    def __init__(self) -> None:
        load_dotenv()
        self.__host = os.getenv("HOST")
        self.__database = os.getenv("DATABASE")
        self.__user = os.getenv("USERNAME")
        self.__password = os.getenv("PASSWORD")
        asyncio.run(self.create_table())

    async def connect(self) -> None:
        """
        Устанавливает соединение с базой данных.
        """
        try:
            self.connection = await asyncpg.connect(
                host=self.__host, database=self.__database, user=self.__user, password=self.__password
            )
        except Exception as ex:
            logger.error(f"{ex.__class__.__name__}: {ex}", exc_info=True)

    async def create_table(self) -> None:
        """
        Создает таблицу user_info в базе данных, если она не существует.
        """
        await self.connect()
        try:
            await self.connection.execute(
                """
                CREATE TABLE IF NOT EXISTS user_info (
                    id SERIAL PRIMARY KEY,
                    user_id TEXT,
                    user_name TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    image_count INT,
                    model TEXT
                )"""
            )
        except Exception as ex:
            logger.debug(f"{ex.__class__.__name__}: {ex}", exc_info=True)
        finally:
            await self.connection.close()

    async def new_user(self, data_user) -> None:
        """
        Метод для добавления нового пользователя в базу данных.

        :param data_user: Объект пользователя, полученный из сообщения.
        """
        await self.connect()
        try:
            user_id = str(data_user.id)
            duplicate = await self.connection.fetchrow("SELECT user_id FROM user_info WHERE user_id = $1", user_id)
            if duplicate is None:
                await self.connection.execute(
                    """
                    INSERT INTO user_info (user_id, user_name, first_name, last_name, image_count, model)
                    VALUES ($1, $2, $3, $4, $5, $6)
                    """,
                    user_id,
                    data_user.username,
                    data_user.first_name,
                    data_user.last_name,
                    0,
                    "u2net",
                )
                logger.info(f"Зарегистрирован новый пользователь: {data_user.username}, {data_user.first_name}")
        except Exception as ex:
            logger.debug(f"{ex.__class__.__name__}: {ex}", exc_info=True)
        finally:
            await self.connection.close()

    async def update_model(self, model_name: str, user_id: str) -> None:
        """
        Метод для обновления модели пользователя в базе данных.

        :param model_name: Новое имя модели пользователя.
        :param user_id: Идентификатор пользователя.
        """
        await self.connect()
        try:
            await self.connection.execute("UPDATE user_info SET model = $1 WHERE user_id = $2", model_name, user_id)
            await self.connection.close()
        except Exception as ex:
            logger.debug(f"{ex.__class__.__name__}: {ex}", exc_info=True)
        finally:
            await self.connection.close()

    async def get_model(self, user_id: str) -> None:
        """
        Метод для получения текущей модели пользователя из базы данных.

        :param user_id: Идентификатор пользователя.
        :return: Имя текущей модели пользователя.
        """
        await self.connect()
        try:
            result = await self.connection.fetchrow("SELECT model FROM user_info WHERE user_id = $1", user_id)
            return result["model"]
        except Exception as ex:
            logger.debug(f"{ex.__class__.__name__}: {ex}", exc_info=True)
        finally:
            await self.connection.close()

    async def set_model(self, user_id: str, model: str) -> None:
        """
        Метод для установки новой модели пользователя в базе данных.

        :param user_id: Идентификатор пользователя.
        :param model: Новая модель пользователя.
        """
        await self.connect()
        try:
            await self.connection.execute("UPDATE user_info SET model = $1 WHERE user_id = $2", model, user_id)
        except Exception as ex:
            logger.debug(f"{ex.__class__.__name__}: {ex}", exc_info=True)
        finally:
            await self.connection.close()
