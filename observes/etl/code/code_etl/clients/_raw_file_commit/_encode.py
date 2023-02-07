from code_etl.clients._raw_objs import (
    RawFileCommitRelation,
)
from fa_purity import (
    FrozenDict,
)
from fa_purity.frozen import (
    freeze,
)
from redshift_client.sql_client.primitive import (
    PrimitiveVal,
)
from typing import (
    Dict,
    Optional,
)


def _to_dict(obj: RawFileCommitRelation) -> Dict[str, Optional[str]]:
    return {
        "file_path": obj.file_path,
        "namespace": obj.namespace,
        "repository": obj.repository,
        "hash": obj.hash,
    }


def primitive_encode(
    row: RawFileCommitRelation,
) -> FrozenDict[str, PrimitiveVal]:
    raw: Dict[str, PrimitiveVal] = {k: v for k, v in _to_dict(row).items()}
    return freeze(raw)
