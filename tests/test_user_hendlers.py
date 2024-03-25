from unittest.mock import AsyncMock

import pytest

from hendlers.user_hendlers import cancel_btn, buy_subscription
from keyboards.inline import buy_subscription_markup
from keyboards.replay import main_markup
from tests.conftest import memory_storage as storage


@pytest.mark.asyncio
async def test_cancel_btn(storage, bot):
    query = AsyncMock()
    await cancel_btn(query)
    assert query.answer.called_once_with(
        f"С возвращением {query.message.from_user.first_name}\n"
        f"Хочеш запонить еще одну анкету❓\n"
        f"\n"
        f"<i>Продолжая, вы принимаете\n"
        f"<a href='...'>Пользовательское соглашение</a> "
        f"и <a href='...'>Политику конфиденциальности</a>.</i>",
        reply_markup=main_markup

    )


@pytest.mark.asyncio
async def test_buy_subscription(storage, bot):
    message = AsyncMock()
    await buy_subscription(message)
    assert message.answer.called_once_with(
        "(Условия подписки)\n", reply_markup=buy_subscription_markup
    )


'''
TODO: доработать тесты для функций edit_questionnaires и delete_questionnaires
@pytest.mark.asyncio
async def test_delete_questionnaires(storage, bot):
    message = AsyncMock()
    await delete_questionnaires(message)
    assert message.answer.called_once_with(
    )'''

'''@pytest.mark.asyncio
async def test_edit_questionnaires(storage, bot):
    message = AsyncMock()
    state = FSMContext(
        storage=storage,
        key=StorageKey(
            bot_id=bot.id,
            user_id=test_user.id,
            chat_id=chat.id,
        ),
    )
    await edit_questionnaires(message, state=state)'''

