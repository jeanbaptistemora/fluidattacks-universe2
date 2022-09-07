# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    GraphShard,
    GraphShardMetadataLanguage as LanguagesEnum,
)
import psutil
from sast.parse import (
    parse_one,
)
from typing import (
    Dict,
    Iterator,
    List,
    Optional,
    Tuple,
)
from utils.fs import (
    decide_language,
    resolve_paths,
    safe_sync_get_file_raw_content,
)


class Paths:
    def __init__(self, include: Tuple[str, ...], exclude: Tuple[str, ...]):
        self.paths_lang: Dict[str, LanguagesEnum] = {}
        self.paths_by_lang: Dict[LanguagesEnum, List[str]] = {
            lang: [] for lang in LanguagesEnum
        }

        self.ok_paths, self.nu_paths, self.nv_paths = resolve_paths(
            include,
            exclude,
        )

    def get_all(self) -> Tuple[str, ...]:
        return self.ok_paths + self.nu_paths + self.nv_paths

    def set_lang(self) -> None:
        for path in self.ok_paths:
            lang = decide_language(path)
            self.paths_lang[path] = lang
            self.paths_by_lang[lang].append(path)


class ShardDb:
    def __init__(self, paths: Paths, threshold: float = 80.0):
        self.paths = paths
        self.threshold: float = threshold
        self.current_paths: List[str] = []
        self.shards: Dict[str, GraphShard] = {}

    def get_memory_usage(self) -> float:
        # pylint: disable=no-self-use
        return psutil.virtual_memory().percent

    def make_space(self) -> None:
        if not self.current_paths:
            raise MemoryError("No memory to store shards")
        del self.shards[self.current_paths.pop(0)]

    def enough_space(self) -> bool:
        return self.get_memory_usage() < self.threshold

    def store_shard(self, path: str) -> None:
        while not self.enough_space():
            self.make_space()

        language = self.paths.paths_lang[path]
        content = safe_sync_get_file_raw_content(path)
        if gs_parsed := parse_one(path, language, content):
            self.shards[path] = gs_parsed
        self.current_paths.append(path)

    def get_shard(self, path: str) -> Optional[GraphShard]:
        if path not in self.shards:
            self.store_shard(path)

        return self.shards[path]

    def iter_lang_shards(self, lang: LanguagesEnum) -> Iterator[GraphShard]:
        for path in self.paths.paths_by_lang[lang]:
            if shard := self.get_shard(path):
                yield shard
