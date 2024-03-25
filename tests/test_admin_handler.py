from unittest.mock import AsyncMock

import pytest
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey

from hendlers.admin_hendlers import (moderation_questionnaires,
                                     not_moderation_questionnaires,
                                     get_questionnaires)
from keyboards.inline import download_button
from tests.conftest import memory_storage as storage
from tests.utils_test import test_user, chat


@pytest.mark.asyncio
async def test_moderation_questionnaires(storage, bot):
    coll = AsyncMock()
    state = FSMContext(
        storage=storage,
        key=StorageKey(
            bot_id=bot.id,
            user_id=test_user.id,
            chat_id=chat.id,
        ),
    )
    await moderation_questionnaires(coll, state=state, bot=bot)
    assert state.get_data() is not None


@pytest.mark.asyncio
async def test_not_moderation_questionnaires():
    coll = AsyncMock()
    await not_moderation_questionnaires(coll)
    coll.answer.assert_called_once_with(
    )


'''TODO доработать тест для next_moderation_questionnaires
@pytest.mark.asyncio
async def test_next_moderation_questionnaires(storage, bot):
    message = AsyncMock()
    state = FSMContext(
        storage=storage,
        key=StorageKey(
            bot_id=bot.id,
            user_id=test_user.id,
            chat_id=chat.id,
        ),
    )
    await next_moderation_questionnaires(message, state=state, bot=bot)'''


@pytest.mark.asyncio
async def test_get_questionnaires():
    message = AsyncMock()
    await get_questionnaires(message)
    message.answer.assert_called_once_with(
        "Можно выгрузить всех пользователей бота (не анкеты).\n"
        "Либо анкеты пользоветелей.",
        reply_markup=download_button
    )
