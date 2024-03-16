import os
import random

from dotenv import load_dotenv

load_dotenv()


def get_random_admin():
    admins_ids = os.environ.get("ADMINS_ID").split(",")
    return random.choice(admins_ids)
