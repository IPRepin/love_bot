import os
import random
from typing import List

from aiogram.filters import BaseFilter
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()


class AdminsFilter(BaseFilter):
    def __init__(self, admin_ids: int | List[int]) -> None:
        self.admin_ids = admin_ids

    async def __call__(self, message: Message) -> bool:
        if isinstance(self.admin_ids, int):
            return message.from_user.id == self.admin_ids
        return message.from_user.id in self.admin_ids


def admins_filter():
    admins = []
    for admin in os.getenv("ADMINS_ID").split(","):
        admins.append(int(admin))
    return admins


def get_random_admin():
    admins_ids = admins_filter()
    return random.choice(admins_ids)
