import aiohttp
import pytest

from aioalfacrm.core import AuthManager, ApiClient

DEFAULT_HOST = 'demo.s20.online'
DEFAULT_EMAIL = 'test@test.test'
DEFAULT_API_KEY = 'api-key'
DEFAULT_BRANCH_ID = 1


@pytest.fixture
@pytest.mark.asyncio
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture(autouse=True)
def add_auth_request(aresponses):
    aresponses.add('demo.s20.online', '/v2api/auth/login', 'POST', {'token': 'api-token'})


@pytest.fixture
def auth_manager(session):
    return AuthManager(
        email=DEFAULT_EMAIL,
        api_key=DEFAULT_API_KEY,
        hostname=DEFAULT_HOST,
        session=session,
    )


@pytest.fixture
def api_client(auth_manager: AuthManager, session):
    return ApiClient(
        hostname=DEFAULT_HOST,
        branch_id=DEFAULT_BRANCH_ID,
        auth_manager=auth_manager,
        session=session,  # noqa
    )
