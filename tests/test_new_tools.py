import pytest
from swarm_x.tools.base import CalculatorTool
from swarm_x.tools.datetime_tool import DateTimeTool
from swarm_x.tools.uuid_tool import UUIDTool

@pytest.mark.asyncio
async def test_calculator_arithmetic():
    result = await CalculatorTool().execute(expression="2 + 3 * (4 - 1)")
    assert result == 11

@pytest.mark.asyncio
async def test_calculator_rejects_non_arithmetic():
    with pytest.raises(Exception):
        await CalculatorTool().execute(expression="__import__('os').system('echo pwned')")

@pytest.mark.asyncio
async def test_datetime_tool_returns_iso_by_default():
    result = await DateTimeTool().execute()
    assert "T" in result

@pytest.mark.asyncio
async def test_uuid_tool_returns_unique_values():
    a = await UUIDTool().execute()
    b = await UUIDTool().execute()
    assert a != b
    assert len(a) == 36
