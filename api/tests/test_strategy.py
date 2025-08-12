import pytest


@pytest.mark.asyncio
async def test_strategy_token_creation(strategy, user):
    token = await strategy.write_token(user)
    assert isinstance(token, str)


@pytest.mark.asyncio
async def test_strategy_token_reading(strategy, user_manager, user):
    token = await strategy.write_token(user)
    read_user = await strategy.read_token(token, user_manager)
    assert str(user.id) == str(read_user.id)
