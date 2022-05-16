from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from more_itertools import (
    split_when,
)
from returns.primitives.hkt import (
    Kind1,
    kinded,
    SupportsKind1,
    SupportsKind2,
)
from tap_gitlab.intervals.alias import (
    NTuple,
)
from tap_gitlab.intervals.fragmented import (
    FIntervalFactory,
    FragmentedInterval,
)
from tap_gitlab.intervals.interval import (
    ClosedInterval,
    OpenInterval,
    OpenLeftInterval,
    OpenRightInterval,
)
from typing import (
    Callable,
    Tuple,
    TypeVar,
)

_DataType = TypeVar("_DataType")
_ProgressIntvlType = TypeVar(
    "_ProgressIntvlType",
    ClosedInterval,
    OpenInterval,
    OpenLeftInterval,
    OpenRightInterval,
)


@dataclass(frozen=True)
class ProgressInterval(
    SupportsKind2["ProgressInterval", _ProgressIntvlType, _DataType],
):
    _interval: Kind1[_ProgressIntvlType, _DataType]
    completed: bool

    # @property do not work here
    @kinded
    def interval(self) -> Kind1[_ProgressIntvlType, _DataType]:
        return self._interval


_State = TypeVar("_State")


@dataclass(frozen=True)
class ProcessStatus(
    SupportsKind2["ProcessStatus", _DataType, _State],
):
    p_intervals: NTuple[ProgressInterval[OpenLeftInterval, _DataType]]
    incomplete_is_present: bool
    function_state: _State


@dataclass(frozen=True)
class _FragmentedProgressInterval(
    SupportsKind1["_FragmentedProgressInterval", _DataType],
):
    f_interval: FragmentedInterval[_DataType]
    completeness: NTuple[bool]


@dataclass(frozen=True)
class FragmentedProgressInterval(
    SupportsKind1["FragmentedProgressInterval", _DataType],
):
    f_interval: FragmentedInterval[_DataType]
    completeness: NTuple[bool]

    def __init__(self, obj: _FragmentedProgressInterval[_DataType]) -> None:
        for key, value in obj.__dict__.items():
            object.__setattr__(self, key, value)

    @property
    def progress_intervals(
        self,
    ) -> NTuple[ProgressInterval[OpenLeftInterval, _DataType]]:
        intervals = zip(self.f_interval.intervals, self.completeness)
        return tuple(
            ProgressInterval(item, completed) for item, completed in intervals
        )

    def process_until_incomplete(
        self,
        function: Callable[
            [_State, ProgressInterval[OpenLeftInterval, _DataType]],
            Tuple[
                _State, NTuple[ProgressInterval[OpenLeftInterval, _DataType]]
            ],
        ],
        init_state: _State,
    ) -> NTuple[ProgressInterval[OpenLeftInterval, _DataType]]:
        def _process(
            prev: ProcessStatus[_DataType, _State],
            interval: ProgressInterval[OpenLeftInterval, _DataType],
        ) -> ProcessStatus[_DataType, _State]:
            if prev.incomplete_is_present:
                return ProcessStatus(
                    (interval,) + prev.p_intervals,
                    prev.incomplete_is_present,
                    prev.function_state,
                )
            state, results = function(prev.function_state, interval)
            incomplete = tuple(
                filter(lambda p_invl: p_invl.completed is False, results)
            )
            return ProcessStatus(
                results + prev.p_intervals, bool(incomplete), state
            )

        status: ProcessStatus[_DataType, _State] = ProcessStatus(
            tuple(), False, init_state
        )
        for interval in reversed(self.progress_intervals):
            status = _process(status, interval)
        return status.p_intervals


class CannotBuild(Exception):
    pass


@dataclass(frozen=True)
class FProgressFactory(
    SupportsKind1["FProgressFactory", _DataType],
):
    factory: FIntervalFactory[_DataType]

    # pylint: disable=no-self-use
    def new_fprogress(
        self,
        f_interval: FragmentedInterval[_DataType],
        completeness: NTuple[bool],
    ) -> FragmentedProgressInterval[_DataType]:
        if len(f_interval.endpoints) - 1 == len(completeness):
            draft = _FragmentedProgressInterval(f_interval, completeness)
            return FragmentedProgressInterval(draft)
        raise CannotBuild("FragmentedProgressInterval")

    def from_n_progress(
        self, progress: NTuple[ProgressInterval[OpenLeftInterval, _DataType]]
    ) -> FragmentedProgressInterval[_DataType]:
        grouped = split_when(
            progress, lambda p1, p2: p1.completed != p2.completed
        )
        compressed = tuple(  # type: ignore
            ProgressInterval(
                self.factory.factory.new_lopen(
                    group[0].interval().lower, group[-1].interval().upper
                ),
                group[0].completed,
            )
            for group in grouped
        )
        intervals: NTuple[OpenLeftInterval[_DataType]] = tuple(
            item.interval() for item in compressed
        )
        f_interval = self.factory.from_intervals(intervals)
        completeness = tuple(item.completed for item in compressed)
        return self.new_fprogress(f_interval, completeness)

    def append(
        self,
        fp_interval: FragmentedProgressInterval[_DataType],
        point: _DataType,
    ) -> FragmentedProgressInterval[_DataType]:
        p_intervals = fp_interval.progress_intervals
        final: OpenLeftInterval[_DataType] = p_intervals[-1].interval()
        new_section = ProgressInterval(  # type: ignore
            self.factory.factory.new_lopen(final.upper, point), False
        )
        return self.from_n_progress(p_intervals + (new_section,))
