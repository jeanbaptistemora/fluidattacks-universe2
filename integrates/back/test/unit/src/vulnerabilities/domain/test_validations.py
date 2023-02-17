from custom_exceptions import (
    InvalidSource,
)
from db_model.enums import (
    Source,
)
import pytest
from vulnerabilities.domain.validations import (
    validate_source_deco,
)

pytestmark = [
    pytest.mark.asyncio,
]


def test_validate_source_deco() -> None:
    @validate_source_deco("source")
    def decorated_func(source: Source) -> Source:
        return source

    assert decorated_func(source="ANALYST")
    with pytest.raises(InvalidSource):
        decorated_func(source="USER")
