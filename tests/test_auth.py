import pytest
from faker import Faker
from httpx import AsyncClient

fake = Faker()


@pytest.mark.asyncio
async def test_register_success(client: AsyncClient):
    user_data = {
        "email": fake.email(),
        "password": "StrongPass123!",
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "phone": fake.phone_number(),
        "role": "MEMBER",
        "department": "TECHNICAL",
    }

    response = await client.post("/auth/register", json=user_data)
    assert response.status_code == 200
    data = response.json()

    assert data["email"] == user_data["email"]
    assert data["first_name"] == user_data["first_name"]
    assert data["last_name"] == user_data["last_name"]
    assert data["role"] == user_data["role"]
    assert data["department"] == user_data["department"]
    assert "id" in data
    assert "password" not in data


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient):
    user_data = {
        "email": fake.email(),
        "password": "StrongPass123!",
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "phone": fake.phone_number(),
        "role": "MEMBER",
        "department": "TECHNICAL",
    }

    response = await client.post("/auth/register", json=user_data)
    assert response.status_code == 200

    response = await client.post("/auth/register", json=user_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


@pytest.mark.asyncio
async def test_register_invalid_data(client: AsyncClient):
    user_data = {"email": fake.email(), "password": "StrongPass123!"}

    response = await client.post("/auth/register", json=user_data)
    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_register_invalid_email(client: AsyncClient):
    user_data = {
        "email": "invalid-email",
        "password": "StrongPass123!",
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "phone": fake.phone_number(),
        "role": "MEMBER",
        "department": "TECHNICAL",
    }

    response = await client.post("/auth/register", json=user_data)
    assert response.status_code == 422
