# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dataclasses import (
    dataclass,
)
from fa_purity import (
    FrozenDict,
    JsonObj,
    JsonValue,
)
from fa_purity.frozen import (
    freeze,
)
from fa_purity.json import (
    factory as JsonFactory,
)
from fa_purity.utils import (
    raise_exception,
)
from fa_singer_io.json_schema import (
    factory as JSchemaFactory,
)
from fa_singer_io.singer import (
    SingerRecord,
    SingerSchema,
)
from tap_mandrill.api.objs.activity import (
    Activity,
)
from tap_mandrill.singer.core import (
    DataStreams,
)
from typing import (
    Dict,
)


@dataclass(frozen=True)
class ActivitySingerEncoder:
    @staticmethod
    def schema() -> SingerSchema:
        # test this property to ensure no failure
        str_type = JSchemaFactory.from_prim_type(str).encode()
        int_type = JSchemaFactory.from_prim_type(int).encode()
        _props: Dict[str, JsonObj] = {
            "date": JSchemaFactory.datetime_schema().encode(),
            "receiver": str_type,
            "sender": str_type,
            "subject": str_type,
            "status": str_type,
            "tags": str_type,
            "subaccount": str_type,
            "opens": int_type,
            "clicks": int_type,
            "bounce": str_type,
        }
        props = FrozenDict({k: JsonValue(v) for k, v in _props.items()})
        raw = {
            "properties": JsonValue(props),
            "required": JsonValue(tuple(JsonValue(k) for k in props.keys())),
        }
        j_schema = JSchemaFactory.from_json(FrozenDict(raw))
        return (
            j_schema.bind(
                lambda j: SingerSchema.new(
                    DataStreams.activity.value,
                    j,
                    frozenset(["date"]),
                    frozenset(),
                )
            )
            .alt(raise_exception)
            .unwrap()
        )

    @staticmethod
    def to_singer(file: Activity) -> SingerRecord:
        return SingerRecord(
            DataStreams.activity.value,
            JsonFactory.from_unfolded_dict(
                freeze(
                    {
                        "date": file.date.isoformat(),
                        "receiver": file.receiver,
                        "sender": file.sender,
                        "subject": file.subject,
                        "status": file.status,
                        "tags": file.tags,
                        "subaccount": file.subaccount,
                        "opens": file.opens,
                        "clicks": file.clicks,
                        "bounce": file.bounce,
                    }
                )
            ),
            None,
        )
