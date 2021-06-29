from __future__ import (
    annotations,
)

from datetime import (
    datetime,
)
from more_itertools import (
    windowed,
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
    Any,
    Callable,
    final,
    Optional,
    Tuple,
    Type,
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


class InvalidInterval(Exception):
    pass


class InvalidEndpoints(Exception):
    pass


_Point = TypeVar("_Point")


def default_greater(_type: Type[_Point]) -> Callable[[_Point, _Point], bool]:
    if isinstance(_type, int):

        def greater_int(_x: int, _y: int) -> bool:
            return _x > _y

        return greater_int
    if isinstance(_type, datetime):

        def greater_dt(_x: datetime, _y: datetime) -> bool:
            return _x > _y

        return greater_dt
    raise NotImplementedError(f"No default greater for type {_type}")


def _common_builder(
    _type: Type[_Point],
    lower: Union[_Point, MIN],
    upper: Union[_Point, MAX],
    greater_than: Optional[Callable[[_Point, _Point], bool]],
) -> Any:
    _greater_than = greater_than if greater_than else default_greater(_type)
    if not isinstance(lower, MIN) and not isinstance(upper, MAX):
        if _greater_than(lower, upper):
            raise InvalidInterval()
    return {
        "lower": lower,
        "upper": upper,
        "greater": _greater_than,
    }


@final
class ClosedInterval(
    BaseContainer,
    SupportsKind1["ClosedInterval", _Point],
):
    def __init__(
        self,
        lower: _Point,
        upper: _Point,
        greater_than: Optional[Callable[[_Point, _Point], bool]] = None,
    ) -> None:
        super().__init__(
            _common_builder(type(lower), lower, upper, greater_than)
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
        _type: Type[_Point],
        lower: Union[_Point, MIN],
        upper: Union[_Point, MAX],
        greater_than: Optional[Callable[[_Point, _Point], bool]] = None,
    ) -> None:
        super().__init__(_common_builder(_type, lower, upper, greater_than))

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
        greater_than: Optional[Callable[[_Point, _Point], bool]] = None,
    ) -> None:
        super().__init__(
            _common_builder(type(upper), lower, upper, greater_than)
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
        greater_than: Optional[Callable[[_Point, _Point], bool]] = None,
    ) -> None:
        super().__init__(
            _common_builder(type(lower), lower, upper, greater_than)
        )

    @property
    def lower(self) -> _Point:
        return self._inner_value["lower"]

    @property
    def upper(self) -> Union[_Point, MAX]:
        return self._inner_value["upper"]


_DataType = TypeVar("_DataType")
Interval = Union[
    ClosedInterval[_DataType],
    OpenInterval[_DataType],
    OpenLeftInterval[_DataType],
    OpenRightInterval[_DataType],
]


@final
class ProgressInterval(
    BaseContainer,
    SupportsKind1["ProgressInterval", _DataType],
):
    def __init__(self, interval: Interval[_DataType], completed: bool) -> None:
        super().__init__(
            {
                "interval": interval,
                "completed": completed,
            }
        )

    @property
    def interval(self) -> Interval[_DataType]:
        return self._inner_value["interval"]

    @property
    def completed(self) -> bool:
        return self._inner_value["completed"]


IntervalPoint = Union[_Point, MIN, MAX]


@final
class FragmentedInterval(
    BaseContainer,
    SupportsKind1["FragmentedInterval", _Point],
):
    def __init__(
        self,
        endpoints: Tuple[IntervalPoint[_Point], ...],
        emptiness: Tuple[bool, ...],
    ) -> None:
        super().__init__(
            {
                "endpoints": endpoints,
                "emptiness": emptiness,
            }
        )

    @property
    def endpoints(self) -> Tuple[IntervalPoint[_Point], ...]:
        return self._inner_value["endpoints"]

    @property
    def emptiness(self) -> Tuple[bool, ...]:
        return self._inner_value["emptiness"]

    @property
    def intervals(self) -> Tuple[OpenLeftInterval[_Point], ...]:
        def _new_interval(
            p_1: Optional[IntervalPoint[_Point]],
            p_2: Optional[IntervalPoint[_Point]],
        ) -> OpenLeftInterval[_Point]:
            if (
                p_1
                and p_2
                and not isinstance(p_1, MAX)
                and not isinstance(p_2, (MIN, MAX))
            ):
                return OpenLeftInterval(p_1, p_2)
            raise InvalidEndpoints()

        return tuple(
            _new_interval(p_1, p_2) for p_1, p_2 in windowed(self.endpoints, 2)
        )

    @property
    def progress_intervals(
        self,
    ) -> Tuple[ProgressInterval[_Point], ...]:
        intervals = zip(self.intervals, self.emptiness)
        return tuple(
            ProgressInterval(item, not empty) for item, empty in intervals
        )

    def to_json(self) -> JSON:
        return {
            "type": "FragmentedInterval",
            "obj": {
                "endpoints": self.endpoints,
                "emptiness": self.emptiness,
            },
        }
