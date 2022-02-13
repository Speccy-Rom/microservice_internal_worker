import pprint

import pytest

from consumer import methods


@pytest.mark.asyncio
async def test_pow_chat_message():
    json_rq = {"username": "test user", "message": "test message", "source": "test",}
    pprint.pprint(json_rq)
    result = await methods.pow_chat_message(json_rq)
    assert result
