from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from singer_io.singer2.json import (
    to_primitive,
)
from typing import (
    Any,
)


@dataclass(frozen=True)
class ProjectId:
    proj_id: str

    @staticmethod
    def from_any(raw: Any) -> ProjectId:
        return ProjectId(to_primitive(raw, str))


@dataclass(frozen=True)
class PostId:
    proj: ProjectId
    post_id: str

    @staticmethod
    def from_any(proj: Any, post: Any) -> PostId:
        return PostId(
            ProjectId.from_any(proj),
            to_primitive(post, str),
        )


@dataclass(frozen=True)
class UserId:
    user_id: str

    @staticmethod
    def from_any(raw: Any) -> UserId:
        return UserId(to_primitive(raw, str))


@dataclass(frozen=True)
class ImageId:
    img_id: str

    @staticmethod
    def from_any(raw: Any) -> ImageId:
        return ImageId(to_primitive(raw, str))
