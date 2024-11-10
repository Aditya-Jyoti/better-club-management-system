import asyncio
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from prisma import Prisma
from typing import AsyncGenerator, Generator
from bcms.main import app
from bcms.database import get_db


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def db() -> AsyncGenerator[Prisma, None]:
    db = Prisma()
    await db.connect()

    await db.auth.delete_many()
    await db.user.delete_many()

    yield db

    await db.disconnect()


@pytest.fixture
async def client(db: Prisma) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
