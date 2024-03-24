import asyncio
import sqlite3
from datetime import datetime

import pytest
import pytest_asyncio
from aiogram import Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage

from tests.mocked_bot import MockedBot
from tests.utils_test import test_user, chat


@pytest_asyncio.fixture()
async def memory_storage():
    storage = MemoryStorage()
    try:
        yield storage
    finally:
        await storage.close()


@pytest.fixture()
def redis_server(request):
    redis_uri = request.config.getoption("--redis")
    return redis_uri


@pytest_asyncio.fixture()
@pytest.mark.redis
async def redis_storage(redis_server):
    if not redis_server:
        pytest.skip("Redis is not available here")
    storage = RedisStorage.from_url(redis_server)
    try:
        await storage.redis.info()
    except ConnectionError as e:
        pytest.skip(str(e))
    try:
        yield storage
    finally:
        conn = await storage.redis
        await conn.flushdb()
        await storage.close()


@pytest.fixture()
def bot():
    return MockedBot()


@pytest_asyncio.fixture()
async def dispatcher():
    dp = Dispatcher()
    await dp.emit_startup()
    try:
        yield dp
    finally:
        await dp.emit_shutdown()


@pytest_asyncio.fixture(scope="session")
async def loop():
    return asyncio.get_event_loop()


@pytest.fixture
def message():
    return types.Message(
        from_user=test_user,
        chat=chat,
        message_id=1,
        date=datetime.now(),
    )


@pytest.fixture
def db_connection():
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
          user_name VARCHAR(255),
          user_id INTEGER NOT NULL,
          user_url VARCHAR(255),
          PRIMARY KEY (user_id)
        );''')
    conn.commit()
    yield conn
    conn.close()


@pytest.fixture
def admins_ids():
    return {
        "ADMINS_ID": "1,2,3",
    }
