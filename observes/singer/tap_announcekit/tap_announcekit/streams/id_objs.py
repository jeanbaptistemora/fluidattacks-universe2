from dataclasses import (
    dataclass,
)


@dataclass(frozen=True)
class ProjectId:
    proj_id: str


@dataclass(frozen=True)
class PostId:
    post_id: str


@dataclass(frozen=True)
class UserId:
    user_id: str


@dataclass(frozen=True)
class ImageId:
    img_id: str
