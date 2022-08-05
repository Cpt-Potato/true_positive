from unittest.mock import AsyncMock

import pytest

from bot.handlers import help_info, show_statistics, start
from bot.keyboard import (
    get_user_keyboard,
    hello_message,
    help_message,
)
from bot.services import check_url


@pytest.mark.asyncio
async def test_check_url():
    assert await check_url("https://www.google.com") is True
    assert await check_url("https://www.goog.lecom") is False


class TestBotEcho:
    @pytest.mark.asyncio
    async def test_start(self):
        message_mock = AsyncMock()
        await start(message=message_mock)
        message_mock.answer.assert_called_with(
            text=hello_message, reply_markup=get_user_keyboard()
        )

    @pytest.mark.asyncio
    async def test_help_info(self):
        message_mock = AsyncMock()
        await help_info(message=message_mock)
        message_mock.answer.assert_called_with(help_message)


class TestDB:
    @pytest.mark.asyncio
    async def test_show_statistics(self):
        message_mock = AsyncMock()
        await show_statistics(message=message_mock)
        message_mock.answer.assert_called_with("Статистика за сегодня пуста")
