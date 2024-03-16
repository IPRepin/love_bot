import os

from aiogram import types
from aiogram.filters import BaseFilter
from dotenv import load_dotenv

load_dotenv()


class AdminFilter(BaseFilter):
    async def check_admin(self, message: types.Message) -> bool:
        return message.from_user.id in os.environ.get("ADMINS_ID").split(",")
