from dataclasses import (
    dataclass,
)
from fa_purity.json import (
    factory as JsonFactory,
)
from fa_purity.json.factory import (
    from_prim_dict,
)
from fa_purity.utils import (
    raise_exception,
)
from fa_singer_io.json_schema import (
    factory as JSchemaFactory,
)
from fa_singer_io.json_schema.core import (
    JsonSchema,
)
from fa_singer_io.singer import (
    SingerRecord,
)
from tap_mandrill.api.objs.activity import (
    Activity,
)
from tap_mandrill.streams.core import (
    DataStreams,
)


@dataclass(frozen=True)
class ActivitySingerEncoder:
    @staticmethod
    @property
    def schema() -> JsonSchema:
        # test this property to ensure no failure
        str_type = JSchemaFactory.from_prim_type(str)
        int_type = JSchemaFactory.from_prim_type(int)
        raw = JsonFactory.from_any(
            {
                "date": JSchemaFactory.datetime_schema(),
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
        ).alt(Exception)
        return raw.bind(JSchemaFactory.from_json).alt(raise_exception).unwrap()

    @staticmethod
    def to_singer(file: Activity) -> SingerRecord:
        return SingerRecord(
            DataStreams.activity.value,
            from_prim_dict(
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
            ),
            None,
        )
