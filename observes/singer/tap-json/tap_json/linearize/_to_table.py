from ._nested_id import (
    struct_hash,
)
from ._non_nested import (
    JsonValueFlatDicts,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    PureIter,
)
from fa_purity.frozen import (
    freeze,
    FrozenDict,
    FrozenList,
)
from fa_purity.json.primitive import (
    Primitive,
)
from fa_purity.pure_iter.factory import (
    from_flist,
)
from fa_purity.union import (
    UnionFactory,
)
from tap_json.clean_str import (
    CleanString,
)
from typing import (
    Callable,
    Dict,
    Generic,
    TypeVar,
)

TABLE_SEP: str = "____"
_T = TypeVar("_T")


@dataclass(frozen=True)
class TableRecordPair:
    table: str
    record: FrozenDict[CleanString, Primitive]


def _list_encode(
    index: int,
    max_index: int,
    value: JsonValueFlatDicts,
    ids: FrozenList[str],
) -> FrozenDict[CleanString, Primitive | FrozenList[JsonValueFlatDicts]]:
    factory: UnionFactory[
        Primitive, FrozenList[JsonValueFlatDicts]
    ] = UnionFactory()
    wrapped_value = value.map(
        lambda v: freeze({CleanString.new("val"): factory.inl(v)}),
        lambda v: freeze({CleanString.new("val"): factory.inr(v)}),
        lambda v: v,
    )
    metadata: Dict[CleanString, Primitive] = {}
    for lvl, this_id in enumerate(ids):
        metadata[CleanString.new(f"sid{lvl}")] = this_id
        metadata[CleanString.new("forward_index")] = index
        metadata[CleanString.new("backward_index")] = max_index - 1 - index
    return freeze(dict(wrapped_value) | metadata)


_ToTablesFunction = Callable[
    [str, JsonValueFlatDicts, FrozenList[str]],
    PureIter[TableRecordPair],
]


@dataclass(frozen=True)
class _Patch(Generic[_T]):
    inner: _T


@dataclass(frozen=True)
class _ToTableRecordsTransform:
    table: str
    ids: FrozenList[str]
    _to_table_patched: _Patch[_ToTablesFunction]

    def _to_table(
        self,
        table: str,
        value: JsonValueFlatDicts,
        ids: FrozenList[str],
    ) -> PureIter[TableRecordPair]:
        return self._to_table_patched.inner(table, value, ids)

    def list_case(
        self,
        items: FrozenList[JsonValueFlatDicts],
    ) -> PureIter[TableRecordPair]:
        return (
            from_flist(items)
            .enumerate(0)
            .map(lambda t: _list_encode(t[0], len(items), t[1], self.ids))
            .map(JsonValueFlatDicts)
            .map(lambda j: self._to_table(self.table, j, self.ids))
            .bind(lambda x: x)
        )

    def _key_val_to_table(
        self,
        key: CleanString,
        value: Primitive | FrozenList[JsonValueFlatDicts],
    ) -> PureIter[TableRecordPair]:
        if isinstance(value, tuple):
            ref_id = struct_hash(JsonValueFlatDicts(value))
            new_table = f"{self.table}{TABLE_SEP}{key.raw}"
            ref = TableRecordPair(
                self.table, freeze({CleanString.new(new_table): ref_id})
            )
            new_ids = self.ids + (ref_id,)
            items = from_flist(
                (
                    from_flist((ref,)),
                    self._to_table(
                        new_table, JsonValueFlatDicts(value), new_ids
                    ),
                )
            )
            return items.bind(lambda x: x)
        result = TableRecordPair(self.table, FrozenDict({key: value}))
        return from_flist((result,))

    def dict_case(
        self,
        items: FrozenDict[
            CleanString, Primitive | FrozenList[JsonValueFlatDicts]
        ],
    ) -> PureIter[TableRecordPair]:
        return (
            from_flist(tuple(items.items()))
            .map(lambda t: self._key_val_to_table(t[0], t[1]))
            .bind(lambda x: x)
        )


def to_table_records(
    table: str,
    value: JsonValueFlatDicts,
    ids: FrozenList[str],
) -> PureIter[TableRecordPair]:
    transform = _ToTableRecordsTransform(table, ids, _Patch(to_table_records))
    return value.map(
        lambda x: to_table_records(
            table, JsonValueFlatDicts(tuple([JsonValueFlatDicts(x)])), ids
        ),
        transform.list_case,
        transform.dict_case,
    )
