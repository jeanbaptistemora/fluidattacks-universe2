from .core import (
    RecordGroup,
    TempReadOnlyFile,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
)
from mypy_boto3_s3.client import (
    S3Client,
)


@dataclass(frozen=True)
class S3FileUploader:
    _client: S3Client
    _bucket: str
    _prefix: str

    def upload_to_s3(
        self, group: RecordGroup, file: TempReadOnlyFile
    ) -> Cmd[None]:
        return file.over_binary(
            lambda f: Cmd.from_cmd(
                lambda: self._client.upload_fileobj(
                    f, self._bucket, self._prefix + group.schema.stream
                )
            )
        )
