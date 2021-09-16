import pytest
from unreliable_indicators import (
    model,
)

# Constants
pytestmark = [
    pytest.mark.asyncio,
]


def test_model_integrity_entity_names() -> None:
    entity_names = list(map(lambda key: str(key), model.ENTITIES.keys()))
    assert entity_names == sorted(entity_names)
