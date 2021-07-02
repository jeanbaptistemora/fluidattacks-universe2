from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from returns.primitives.hkt import (
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
    Interval,
    OpenLeftInterval,
)
from typing import (
    Callable,
    List,
    Tuple,
    TypeVar,
)

_DataType = TypeVar("_DataType")


@dataclass(frozen=True)
class ProgressInterval(
    SupportsKind1["ProgressInterval", _DataType],
):
    interval: Interval[_DataType]
    completed: bool


_State = TypeVar("_State")


@dataclass(frozen=True)
class ProcessStatus(
    SupportsKind2["ProcessStatus", _DataType, _State],
):
    p_intervals: NTuple[ProgressInterval[_DataType]]
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
    ) -> NTuple[ProgressInterval[_DataType]]:
        intervals = zip(self.f_interval.intervals, self.completeness)
        return tuple(
            ProgressInterval(item, completed) for item, completed in intervals
        )

    def process_until_incomplete(
        self,
        function: Callable[
            [_State, ProgressInterval[_DataType]],
            Tuple[_State, NTuple[ProgressInterval[_DataType]]],
        ],
        init_state: _State,
    ) -> NTuple[ProgressInterval[_DataType]]:
        def _process(
            prev: ProcessStatus[_DataType, _State],
            interval: ProgressInterval[_DataType],
        ) -> ProcessStatus[_DataType, _State]:
            if prev.incomplete_is_present:
                return ProcessStatus(
                    prev.p_intervals + (interval,),
                    prev.incomplete_is_present,
                    prev.function_state,
                )
            state, results = function(prev.function_state, interval)
            incomplete = tuple(
                filter(lambda p_invl: p_invl.completed is False, results)
            )
            return ProcessStatus(
                prev.p_intervals + results, bool(incomplete), state
            )

        status: ProcessStatus[_DataType, _State] = ProcessStatus(
            tuple(), False, init_state
        )
        for interval in self.progress_intervals:
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
        self, progress: NTuple[ProgressInterval[_DataType]]
    ) -> FragmentedProgressInterval[_DataType]:
        _progress: List[Tuple[OpenLeftInterval[_DataType], bool]] = []
        for item in progress:
            if isinstance(item.interval, OpenLeftInterval):
                _progress.append((item.interval, item.completed))
            else:
                raise CannotBuild("Expected OpenLeftInterval")
        intervals = tuple(item[0] for item in _progress)
        f_interval = self.factory.from_intervals(intervals)
        completeness = tuple(item[1] for item in _progress)
        return self.new_fprogress(f_interval, completeness)
