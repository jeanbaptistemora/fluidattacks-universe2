# pylint: disable=unnecessary-lambda
# necessary for type checking
from dataclasses import (
    dataclass,
)
from paginator.v2 import (
    IntIndexGetter,
)
from purity.v1 import (
    Flattener,
    FrozenList,
    PureIter,
)
from purity.v1.pure_iter.factory import (
    from_flist,
    infinite_range,
)
from purity.v1.pure_iter.transform import (
    io as io_transform,
)
from returns.io import (
    IO,
)
from returns.maybe import (
    Maybe,
)
from singer_io.singer2 import (
    SingerEmitter,
    SingerRecord,
)
from tap_checkly.api2.checks import (
    ChecksApi,
)
from tap_checkly.api2.objs.check.result import (
    RolledUpResultObj,
)
from tap_checkly.api2.objs.id_objs import (
    CheckId,
)
from tap_checkly.streams.checks_rolled_up._encode import (
    to_singer,
)


@dataclass(frozen=True)
class ChkRollStream:
    _api: ChecksApi
    _emitter: SingerEmitter
    main_stream_name: str
    times_stream_name: str

    def _get_page(
        self, check: CheckId, page: int
    ) -> IO[Maybe[FrozenList[RolledUpResultObj]]]:
        return self._api.rolled_up_results(check, page).map(
            lambda p: Maybe.from_optional(p if len(p) > 0 else None)
        )

    def _check_all_rolled_up(
        self, check: CheckId
    ) -> PureIter[IO[RolledUpResultObj]]:
        getter: IntIndexGetter[FrozenList[RolledUpResultObj]] = IntIndexGetter(
            lambda p: self._get_page(check, p)
        )
        pages = (
            infinite_range(1, 1)
            .chunked(10)
            .map(lambda i: tuple(i))
            .map(getter.get_pages)
        ).map(lambda io_items: io_items.map(lambda i: from_flist(i)))
        result = io_transform.until_empty(io_transform.chain(pages)).map(
            lambda i: i.map(lambda j: from_flist(j))
        )
        return io_transform.chain(result)

    def records(self, check: CheckId) -> PureIter[IO[SingerRecord]]:
        return io_transform.chain(
            self._check_all_rolled_up(check).map(
                lambda i: i.map(
                    lambda n: to_singer(
                        self.main_stream_name, self.times_stream_name, n
                    )
                ).map(lambda i: from_flist(i))
            )
        )

    def _all_ids(self) -> PureIter[IO[CheckId]]:
        getter: IntIndexGetter[FrozenList[CheckId]] = IntIndexGetter(
            lambda p: self._api.ids(p).map(
                lambda i: Maybe.from_optional(i if len(i) > 0 else None)
            )
        )
        pages = (
            infinite_range(1, 1)
            .chunked(10)
            .map(lambda i: tuple(i))
            .map(getter.get_pages)
        ).map(lambda io_items: io_items.map(lambda i: from_flist(i)))
        result = io_transform.until_empty(io_transform.chain(pages)).map(
            lambda i: i.map(lambda j: from_flist(j))
        )
        return io_transform.chain(result)

    def emit(self) -> IO[None]:
        ids = self._all_ids()
        records = io_transform.chain(
            ids.map(lambda i: i.map(self.records))
        ).map(lambda i: Flattener.denest(i))
        return io_transform.consume(
            records.map(lambda i: i.bind(self._emitter.emit))
        )
