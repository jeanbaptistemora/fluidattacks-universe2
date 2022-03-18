from model.graph_model import (
    GraphShardMetadataLanguage as LanguagesEnum,
)
from typing import (
    Dict,
    List,
    Tuple,
)
from utils.fs import (
    decide_language,
    resolve_paths,
)


class Paths:
    def __init__(self, include: Tuple[str, ...], exclude: Tuple[str, ...]):
        self.paths_by_lang: Dict[LanguagesEnum, List[str]] = {
            lang: [] for lang in LanguagesEnum
        }

        self.ok_paths, self.nu_paths, self.nv_paths = resolve_paths(
            include,
            exclude,
        )

    def get_all(self) -> Tuple[str, ...]:
        return self.ok_paths + self.nu_paths + self.nv_paths

    def set_paths_by_lang(self) -> None:
        for path in self.ok_paths:
            self.paths_by_lang[decide_language(path)].append(path)
