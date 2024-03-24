import os
from unittest.mock import AsyncMock, patch

import pytest

from hendlers.hendler_commands import help_command, get_start


@pytest.mark.asyncio
async def test_cmd_help():
    message = AsyncMock()
    await help_command(message)

    message.answer.assert_called_once_with(f"- /start - Начать заполнение анкеты;\n")


@pytest.mark.asyncio
async def test_get_start(message, db_connection, admins_ids):
    pass