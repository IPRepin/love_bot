from unittest.mock import AsyncMock

import pytest

from hendlers.hendler_commands import help_command, get_start


@pytest.mark.asyncio
async def test_cmd_help():
    message = AsyncMock()
    await help_command(message)

    message.answer.assert_called_once_with(f"- /start - Начать заполнение анкеты;\n")


# async def test_cmd_start():
#     await get_start(message)