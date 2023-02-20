from custom_exceptions import (
    InvalidPath,
    InvalidSource,
    InvalidVulnWhere,
)
from db_model.enums import (
    Source,
)
import pytest
from vulnerabilities.domain.validations import (
    validate_path_deco,
    validate_source_deco,
    validate_where_deco,
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


def test_validate_path_deco() -> None:
    @validate_path_deco("path")
    def decorated_func(path: str) -> str:
        return path

    assert decorated_func(path="C:/Program Files/MyApp")
    with pytest.raises(InvalidPath):
        decorated_func(path="C:\\Program Files\\MyApp")


def test_validate_where_deco() -> None:
    @validate_where_deco("where")
    def decorated_func(where: str) -> str:
        return where

    assert decorated_func(where="MyVulnerability")
    with pytest.raises(InvalidVulnWhere):
        decorated_func(where="=MyVulnerability")
