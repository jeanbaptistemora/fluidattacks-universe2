# SPDX-FileCopyrightText: 2022 "Fluid Attacks <development@fluidattacks.com>"
#
# SPDX-License-Identifier: MPL-2.0

from code_etl.client._raw_objs import (
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
        "file": obj.file_path,
        "namespace": obj.namespace,
        "repository": obj.repository,
        "hash": obj.hash,
    }


def primitive_encode(
    row: RawFileCommitRelation,
) -> FrozenDict[str, PrimitiveVal]:
    raw: Dict[str, PrimitiveVal] = {k: v for k, v in _to_dict(row).items()}
    return freeze(raw)
