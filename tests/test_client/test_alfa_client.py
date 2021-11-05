import aiohttp
import pytest

try:
    from unittest.mock import AsyncMock as CoroutineMock, patch
except ImportError:
    from asynctest import CoroutineMock, patch

from aioalfacrm import AlfaClient


@pytest.mark.asyncio
async def test_init():
    client = AlfaClient(
        hostname='demo.s20.online',
        email='test@test.example',
        api_key='api-key',
        branch_id=1,
    )
    assert client.hostname == 'demo.s20.online'
    assert client.email == 'test@test.example'
    assert client.api_key == 'api-key'
    assert client.branch_id == 1


@pytest.mark.asyncio
async def test_close():
    session = aiohttp.ClientSession()
    client = AlfaClient(
        hostname='demo.s20.online',
        email='test@test.example',
        api_key='api_key',
        branch_id=1,
        session=session,
    )

    with patch('aiohttp.ClientSession.close', new_callable=CoroutineMock) as mocked_close:
        await client.close()
        mocked_close.assert_awaited()
