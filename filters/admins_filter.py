import os
import random
from typing import List

from aiogram.filters import BaseFilter
from aiogram.types import Message

from dotenv import load_dotenv

load_dotenv()


def get_random_admin():
    admins_ids = os.environ.get("ADMINS_ID").split(",")
    return random.choice(admins_ids)


class AdminsFilter(BaseFilter):
    def __init__(self, admin_ids: int | List[int]) -> None:
        self.admin_ids = admin_ids

    async def __call__(self, message: Message) -> bool:
        if isinstance(self.admin_ids, int):
            return message.from_user.id == self.admin_ids
        return message.from_user.id in self.admin_ids
