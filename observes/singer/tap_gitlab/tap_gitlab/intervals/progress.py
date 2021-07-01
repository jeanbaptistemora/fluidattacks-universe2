from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
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
)
from typing import (
    Callable,
    final,
    Generic,
    Tuple,
    TypeVar,
)

_DataType = TypeVar("_DataType")


@final
@dataclass(frozen=True)
class ProgressInterval(Generic[_DataType]):
    interval: Interval[_DataType]
    completed: bool


_State = TypeVar("_State")


@final
@dataclass(frozen=True)
class ProcessStatus(Generic[_DataType, _State]):
    p_intervals: NTuple[ProgressInterval[_DataType]]
    incomplete_is_present: bool
    function_state: _State


@final
@dataclass(frozen=True)
class _FragmentedProgressInterval(Generic[_DataType]):
    f_interval: FragmentedInterval[_DataType]
    completeness: NTuple[bool]


@final
@dataclass(frozen=True)
class FragmentedProgressInterval(Generic[_DataType]):
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


@final
@dataclass(frozen=True)
class FProgressFactory(Generic[_DataType]):
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
