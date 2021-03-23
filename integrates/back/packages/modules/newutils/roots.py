# Standard libraries
from typing import Tuple

# Local libraries
from backend.exceptions import (
    RootNotFound,
)
from backend.typing import (
    GitRoot,
    Root,
)


def get_root_id_by_filename(
    filename: str,
    group_roots: Tuple[Root, ...]
) -> str:
    root_nickname = filename.split('/')[0]
    file_name_root_ids = [
        root.id
        for root in group_roots
        if isinstance(root, GitRoot)
        and root.nickname == root_nickname
    ]
    if not file_name_root_ids:
        raise RootNotFound()
    file_name_root_id = file_name_root_ids[0]

    return file_name_root_id
