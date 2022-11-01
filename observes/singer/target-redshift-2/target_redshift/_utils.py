# SPDX-FileCopyrightText: 2022 "Fluid Attacks <development@fluidattacks.com>"
#
# SPDX-License-Identifier: MPL-2.0

from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from fa_purity import (
    Result,
    ResultE,
)


@dataclass(frozen=True)
class S3FileObjURI:
    bucket: str
    file_name: str

    @staticmethod
    def from_raw(raw: str) -> ResultE[S3FileObjURI]:
        try:
            if raw.startswith("s3://"):
                _splitted = raw.split("/")
                bucket = "/".join(_splitted[:-1])
                obj_file = _splitted[-1]
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
        return "/".join([self.bucket, self.file_name])
