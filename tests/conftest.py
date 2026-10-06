import pytest_asyncio
from apps.api.database import init_db

@pytest_asyncio.fixture(autouse=True)
async def prepare_database():
    await init_db()
