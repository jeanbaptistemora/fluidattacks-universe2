from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
    FrozenDict,
    Result,
    ResultE,
)
from redshift_client.sql_client import (
    Query,
    QueryValues,
    SqlClient,
)


@dataclass(frozen=True)
class S3FileObjURI:
    bucket: str
    file_path: str

    @staticmethod
    def from_raw(raw: str) -> ResultE[S3FileObjURI]:
        try:
            if raw.startswith("s3://"):
                _raw = raw.removeprefix("s3://")
                _splitted = _raw.split("/")
                bucket = _splitted[0]
                obj_file = "/".join(_splitted[1:])
                if obj_file:
                    return Result.success(
                        S3FileObjURI(bucket, obj_file), Exception
                    )
            return Result.failure(
                ValueError("Invalid s3 file obj URI"), S3FileObjURI
            ).alt(Exception)
        except IndexError as err:
            return Result.failure(err, S3FileObjURI).alt(Exception)

    def __repr__(self) -> str:
        return "/".join([self.bucket, self.file_path])


def set_queue_group(client: SqlClient, group: str) -> Cmd[None]:
    statement = "SET query_group TO %(group)s"
    args = QueryValues(FrozenDict({"group": group}))
    return client.execute(Query.new_query(statement), args)
