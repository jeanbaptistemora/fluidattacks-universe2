from model.graph_model import (
    GraphShardMetadataLanguage as LanguagesEnum,
)
from utils.fs import (
    decide_language,
    resolve_paths,
)


class Paths:
    def __init__(self, include: tuple[str, ...], exclude: tuple[str, ...]):
        self.paths_lang: dict[str, LanguagesEnum] = {}
        self.paths_by_lang: dict[LanguagesEnum, list[str]] = {
            lang: [] for lang in LanguagesEnum
        }

        self.ok_paths, self.nu_paths, self.nv_paths = resolve_paths(
            include,
            exclude,
        )

    def get_all(self) -> tuple[str, ...]:
        return self.ok_paths + self.nu_paths + self.nv_paths

    def set_lang(self) -> None:
        for path in self.ok_paths:
            lang = decide_language(path)
            self.paths_lang[path] = lang
            self.paths_by_lang[lang].append(path)
