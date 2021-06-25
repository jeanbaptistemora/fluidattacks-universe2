from __future__ import (
    annotations,
)

from returns.primitives.container import (
    BaseContainer,
)
from returns.primitives.hkt import (
    SupportsKind1,
)
from returns.primitives.types import (
    Immutable,
)
from singer_io.common import (
    JSON,
)
from typing import (
    final,
    Tuple,
    TypeVar,
    Union,
)


class MIN(Immutable):
    def __new__(cls) -> MIN:
        return object.__new__(cls)

    def __str__(self) -> str:
        return "MIN"


class MAX(Immutable):
    def __new__(cls) -> MAX:
        return object.__new__(cls)

    def __str__(self) -> str:
        return "MAX"


_Point = TypeVar("_Point")


@final
class ClosedInterval(
    BaseContainer,
    SupportsKind1["ClosedInterval", _Point],
):
    def __init__(
        self,
        lower: _Point,
        upper: _Point,
    ) -> None:
        super().__init__(
            {
                "lower": lower,
                "upper": upper,
            }
        )

    @property
    def lower(self) -> _Point:
        return self._inner_value["lower"]

    @property
    def upper(self) -> _Point:
        return self._inner_value["upper"]


@final
class OpenInterval(
    BaseContainer,
    SupportsKind1["OpenInterval", _Point],
):
    def __init__(
        self,
        lower: Union[_Point, MIN],
        upper: Union[_Point, MAX],
    ) -> None:
        super().__init__(
            {
                "lower": lower,
                "upper": upper,
            }
        )

    @property
    def lower(self) -> Union[_Point, MIN]:
        return self._inner_value["lower"]

    @property
    def upper(self) -> Union[_Point, MAX]:
        return self._inner_value["upper"]


@final
class OpenLeftInterval(
    BaseContainer,
    SupportsKind1["OpenLeftInterval", _Point],
):
    def __init__(
        self,
        lower: Union[_Point, MIN],
        upper: _Point,
    ) -> None:
        super().__init__(
            {
                "lower": lower,
                "upper": upper,
            }
        )

    @property
    def lower(self) -> Union[_Point, MIN]:
        return self._inner_value["lower"]

    @property
    def upper(self) -> _Point:
        return self._inner_value["upper"]


@final
class OpenRightInterval(
    BaseContainer,
    SupportsKind1["OpenRightInterval", _Point],
):
    def __init__(
        self,
        lower: _Point,
        upper: Union[_Point, MAX],
    ) -> None:
        super().__init__(
            {
                "lower": lower,
                "upper": upper,
            }
        )

    @property
    def lower(self) -> _Point:
        return self._inner_value["lower"]

    @property
    def upper(self) -> Union[_Point, MAX]:
        return self._inner_value["upper"]


@final
class FragmentedInterval(
    BaseContainer,
    SupportsKind1["FragmentedInterval", _Point],
):
    def __init__(
        self,
        endpoints: Tuple[_Point, ...],
        emptiness: Tuple[bool, ...],
    ) -> None:
        super().__init__(
            {
                "endpoints": endpoints,
                "emptiness": emptiness,
            }
        )

    @property
    def endpoints(self) -> Tuple[_Point, ...]:
        return self._inner_value["endpoints"]

    @property
    def emptiness(self) -> Tuple[bool, ...]:
        return self._inner_value["emptiness"]

    def to_json(self) -> JSON:
        return {
            "type": "FragmentedInterval",
            "obj": {
                "endpoints": self.endpoints,
                "emptiness": self.emptiness,
            },
        }
