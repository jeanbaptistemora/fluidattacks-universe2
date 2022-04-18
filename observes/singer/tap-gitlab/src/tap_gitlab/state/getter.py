# pylint: skip-file
from dataclasses import (
    dataclass,
)
import json
from returns.maybe import (
    Maybe,
    Nothing,
)
from tap_gitlab.state._objs import (
    EtlState,
)
from tap_gitlab.state.decoder import (
    StateDecoder,
)
import tempfile
from typing import (
    Any,
)


def _obj_exist(s3_client: Any, bucket: str, key: str) -> bool:
    try:
        s3_client.get_object(Bucket=bucket, Key=key)
        return True
    except (s3_client.exceptions.NoSuchBucket, s3_client.exceptions.NoSuchKey):
        return False


@dataclass(frozen=True)
class StateGetter:
    s3_client: Any
    decoder: StateDecoder

    def get(self, bucket: str, obj_key: str) -> Maybe[EtlState]:
        if _obj_exist(self.s3_client, bucket, obj_key):
            with tempfile.TemporaryFile() as temp:
                self.s3_client.download_fileobj(bucket, obj_key, temp)
                temp.seek(0)
                raw = json.load(temp)
                return Maybe.from_value(self.decoder.decode_etl_state(raw))
        return Nothing
