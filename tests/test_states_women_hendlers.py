from unittest.mock import AsyncMock

import pytest
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey

from hendlers.states_woman import (
    add_photo,
    incorrect_photo,
    add_age,
    add_about,
    add_find_me,
    check_status,
    incorrect_gender,
)
from keyboards.replay import gen_replay_keyboard
from tests.conftest import memory_storage as storage
from tests.utils_test import test_user, chat
from utils.states import StatesWomanQuestionnaire


@pytest.mark.asyncio
async def test_men_state_add_photo(storage, bot):
    message = AsyncMock()
    state = FSMContext(
        storage=storage,
        key=StorageKey(
            bot_id=bot.id,
            user_id=test_user.id,
            chat_id=chat.id,
        ),
    )
    await add_photo(message, state=state)
    assert await state.get_state() == StatesWomanQuestionnaire.PHOTO
    message.answer.assert_called_once_with(
        f"{message.from_user.first_name}\n"
        "Для начала загрузите свою фотографию!"
    )


'''TODO доработать тест для добавления имени пользователя
@pytest.mark.asyncio
async def test_men_state_add_name(storage, bot):
    message = AsyncMock()
    state = FSMContext(
        storage=storage,
        key=StorageKey(
            bot_id=bot.id,
            user_id=test_user.id,
            chat_id=chat.id,
        ),
    )
    await add_name(message, state=state, bot=bot)
    assert await state.get_state() == StatesMenQuestionnaire.NAME'''


@pytest.mark.asyncio
async def test_men_state_incorrect_photo(storage, bot):
    message = AsyncMock()
    state = FSMContext(
        storage=storage,
        key=StorageKey(
            bot_id=bot.id,
            user_id=test_user.id,
            chat_id=chat.id,
        ),
    )
    await incorrect_photo(message, state=state)
    message.answer.assert_called_once_with(
        f"{message.from_user.first_name}\n"
        "Нужно загрузить фотографию!"
    )


@pytest.mark.asyncio
async def test_men_state_add_age(storage, bot):
    message = AsyncMock()
    state = FSMContext(
        storage=storage,
        key=StorageKey(
            bot_id=bot.id,
            user_id=test_user.id,
            chat_id=chat.id,
        ),
    )
    await add_age(message, state=state)
    assert await state.get_state() == StatesWomanQuestionnaire.AGE
    message.answer.assert_called_once_with(
        "Введите ваш возраст: "
    )


@pytest.mark.asyncio
async def test_men_state_add_about(storage, bot):
    message = AsyncMock()
    state = FSMContext(
        storage=storage,
        key=StorageKey(
            bot_id=bot.id,
            user_id=test_user.id,
            chat_id=chat.id,
        ),
    )
    await add_about(message, state=state)


@pytest.mark.asyncio
async def test_men_state_add_find_me(storage, bot):
    message = AsyncMock()
    state = FSMContext(
        storage=storage,
        key=StorageKey(
            bot_id=bot.id,
            user_id=test_user.id,
            chat_id=chat.id,
        ),
    )
    await add_find_me(message, state=state)
    assert await state.get_state() == StatesWomanQuestionnaire.FIND
    menu = await gen_replay_keyboard(['Парень', 'Девушка'])
    message.answer.assert_called_once_with(
        "Кого вы хотите найти?", reply_markup=menu
    )


@pytest.mark.asyncio
async def test_men_state_check_status(storage, bot):
    message = AsyncMock()
    state = FSMContext(
        storage=storage,
        key=StorageKey(
            bot_id=bot.id,
            user_id=test_user.id,
            chat_id=chat.id,
        ),
    )
    await check_status(message, state=state)
    assert await state.get_state() == StatesWomanQuestionnaire.STATUS
    menu = await gen_replay_keyboard(['Только телеграм'])
    message.answer.assert_called_once_with("Здесь вы можете оставить свой никнейм в любой из соц сетей\n"
                                           "либо нажмите на кнопку ниже если хотите оставить только телеграм.",
                                           reply_markup=menu)


'''
TODO доработать тест для финишного состояния
@pytest.mark.asyncio
async def test_men_state_finish_state(storage, bot):
    message = AsyncMock()
    state = FSMContext(
        storage=storage,
        key=StorageKey(
            bot_id=bot.id,
            user_id=test_user.id,
            chat_id=chat.id,
        ),
    )
    await finish_state(message, state=state, bot=bot)
    '''


@pytest.mark.asyncio
async def test_men_state_incorrect_gender(storage, bot):
    message = AsyncMock()
    state = FSMContext(
        storage=storage,
        key=StorageKey(
            bot_id=bot.id,
            user_id=test_user.id,
            chat_id=chat.id,
        ),
    )
    await incorrect_gender(message, state=state)
    menu = await gen_replay_keyboard(['Парень', 'Девушка'])
    message.answer.assert_called_once_with(
        "Выберите кого вы хотите найти!", reply_markup=menu
    )
