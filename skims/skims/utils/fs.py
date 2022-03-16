import aiofiles  # type: ignore
from concurrent.futures import (
    ThreadPoolExecutor,
)
from fnmatch import (
    fnmatch as matches_glob,
)
from glob import (
    iglob as glob,
)
from itertools import (
    chain,
)
from model.core_model import (
    Paths,
)
from model.graph_model import (
    GraphShardMetadataLanguage,
)
from more_itertools import (
    collapse,
)
from multiprocessing import (
    cpu_count,
)
from operator import (
    attrgetter,
    methodcaller,
)
import os
from pyparsing import (
    Regex,
)
from typing import (
    Awaitable,
    Callable,
    Dict,
    Iterable,
    Iterator,
    List,
    Set,
    Tuple,
)
from utils.logs import (
    log_blocking,
)

MAX_FILE_SIZE: int = 102400  # 100KiB


class FileTooLarge(Exception):
    pass


language_extensions_map: Dict[GraphShardMetadataLanguage, List[str]] = {
    GraphShardMetadataLanguage.CSHARP: [".cs"],
    GraphShardMetadataLanguage.GO: [".go"],
    GraphShardMetadataLanguage.JAVA: [".java"],
    GraphShardMetadataLanguage.JAVASCRIPT: [".js", ".jsx"],
    GraphShardMetadataLanguage.KOTLIN: [".kt", ".ktm", ".kts"],
    GraphShardMetadataLanguage.PHP: [".php"],
    GraphShardMetadataLanguage.RUBY: [".rb"],
    GraphShardMetadataLanguage.SCALA: [".sc", ".scala"],
    GraphShardMetadataLanguage.TSX: [".ts", ".tsx"],
}


def decide_language(path: str) -> GraphShardMetadataLanguage:
    for language, extensions in language_extensions_map.items():
        for extension in extensions:
            if path.endswith(extension):
                return language
    return GraphShardMetadataLanguage.NOT_SUPPORTED


def generate_file_content(
    path: str,
    encoding: str = "latin-1",
    size: int = -1,
) -> Callable[[], str]:
    data: Dict[str, str] = {}

    def get_one() -> str:
        if not data:
            data["file_contents"] = get_file_content_block(
                path=path,
                encoding=encoding,
                size=size,
            )
        return data["file_contents"]

    return get_one


def generate_file_raw_content(
    path: str,
    size: int = -1,
) -> Callable[[], Awaitable[bytes]]:
    data: Dict[str, bytes] = {}

    async def get_one() -> bytes:
        if not data:
            data["file_raw_content"] = await get_file_raw_content(path, size)
        return data["file_raw_content"]

    return get_one


def generate_file_raw_content_blocking(
    path: str,
    size: int = -1,
) -> Callable[[], bytes]:
    data: Dict[str, bytes] = {}

    def get_one() -> bytes:
        if not data:
            data["file_raw_content"] = get_file_raw_content_blocking(
                path, size
            )
        return data["file_raw_content"]

    return get_one


async def get_file_content(
    path: str,
    encoding: str = "latin-1",
    size: int = -1,
) -> str:
    async with aiofiles.open(
        path,
        mode="r",
        encoding=encoding,
    ) as file_handle:
        file_contents: str = await file_handle.read(size)

        return file_contents


def get_file_content_block(
    path: str,
    encoding: str = "latin-1",
    size: int = -1,
) -> str:
    with open(
        path,
        mode="r",
        encoding=encoding,
    ) as file_handle:
        file_contents: str = file_handle.read(size)

        return file_contents


def sync_get_file_content(path: str, size: int = MAX_FILE_SIZE) -> str:
    if os.stat(path).st_size > MAX_FILE_SIZE:
        raise FileTooLarge(path)

    with open(path, mode="r", encoding="latin-1") as handle:
        content = handle.read(size)

    return content


async def get_file_raw_content(path: str, size: int = -1) -> bytes:
    async with aiofiles.open(path, mode="rb") as file_handle:
        file_contents: bytes = await file_handle.read(size)

        return file_contents


def get_file_raw_content_blocking(path: str, size: int = -1) -> bytes:
    with open(path, mode="rb") as file_handle:
        file_contents: bytes = file_handle.read(size)

        return file_contents


def sync_get_file_raw_content(path: str, size: int = MAX_FILE_SIZE) -> bytes:
    if os.stat(path).st_size > MAX_FILE_SIZE:
        raise FileTooLarge(path)

    with open(path, "rb") as handle:
        content = handle.read(size)

    return content


def check_dependency_code(path: str) -> bool:
    language: GraphShardMetadataLanguage = decide_language(path)

    if language == GraphShardMetadataLanguage.JAVASCRIPT:
        regex_exp = [
            Regex(r"jQuery(.)*[Cc]opyright(.)*[Ll]icen"),
            Regex(r"[Cc]opyright(.)*[Ll]icen(.)*[Jj][Qq]uery"),
            Regex(r"[Aa]ngular[Jj][Ss](.)*[Gg]oogle(.)*[Ll]icen"),
        ]
    else:
        return False

    file_content = generate_file_content(path, size=200)
    raw_content = file_content()
    content = raw_content.replace("\n", " ")

    for regex in regex_exp:
        for _ in regex.scanString(content):
            return True
    return False


def get_non_upgradable_paths(paths: Set[str]) -> Set[str]:
    nu_paths: Set[str] = set()

    intellisense_refs = {
        os.path.dirname(path)
        for path in paths
        if path.endswith("Scripts/_references.js")
    }

    for path in paths:
        if (
            any(
                path.startswith(intellisense_ref)
                for intellisense_ref in intellisense_refs
            )
            or any(
                matches_glob(f"/{path}", glob)
                for glob in (
                    "*/Assets*/vendor/*",
                    "*/Assets*/lib/*",
                    "*/Assets*/js/*",
                    "*/Content*/jquery*",
                    "*/GoogleMapping*.js",
                    "*/Scripts*/bootstrap*",
                    "*/Scripts*/modernizr*",
                    "*/Scripts*/jquery*",
                    "*/Scripts*/popper*",
                    "*/Scripts*/vue*",
                    "*/wwwroot/lib*",
                )
            )
            or check_dependency_code(path)
        ):
            nu_paths.add(path)

    return nu_paths


def get_non_verifiable_paths(paths: Set[str]) -> Set[str]:
    nv_paths: Set[str] = set()

    for path in paths:
        _, file = os.path.split(path)
        file_name, file_extension = os.path.splitext(file)
        file_extension = file_extension[1:]

        if (
            file_extension
            in {
                "aar",
                "apk",
                "bin",
                "class",
                "dll",
                "DS_Store",
                "exec",
                "hprof",
                "jar",
                "jasper",
                "pdb",
                "pyc",
                "exe",
            }
            or (file_name, file_extension)
            in {
                ("debug", "log"),
                ("org.eclipse.buildship.core.prefs"),
                (".classpath", ""),
                (".project", ""),
                (".vscode", ""),
            }
            or any(
                path.endswith(end)
                for end in (
                    ".cs.bak",
                    ".csproj.bak",
                    ".min.js",
                )
            )
            or any(
                string in path
                for string in (
                    "/.serverless_plugins/",
                    "/.settings/",
                )
            )
        ):
            nv_paths.add(path)

    return nv_paths


def mkdir(name: str, mode: int = 0o777, exist_ok: bool = False) -> None:
    return os.makedirs(name, mode=mode, exist_ok=exist_ok)


def recurse_dir(path: str) -> Tuple[str, ...]:
    try:
        scanner = tuple(os.scandir(path))
    except FileNotFoundError:
        scanner = tuple()

    dirs = tuple(
        map(attrgetter("path"), filter(methodcaller("is_dir"), scanner))
    )
    files = tuple(
        map(attrgetter("path"), filter(methodcaller("is_file"), scanner))
    )
    with ThreadPoolExecutor(max_workers=cpu_count()) as _worker:
        tree = tuple(
            chain(
                files,
                _worker.map(recurse_dir, dirs),
            )
        )

    return tree


def recurse(path: str) -> Tuple[str, ...]:
    return (path,) if os.path.isfile(path) else recurse_dir(path)


def resolve_paths(
    *,
    exclude: Tuple[str, ...],
    include: Tuple[str, ...],
) -> Paths:
    def evaluate_glob(path: str) -> Iterable[str]:
        if path.startswith("glob(") and path.endswith(")"):
            yield from glob(path[5:-1], recursive=True)
        else:
            yield path

    def evaluate(wkr: ThreadPoolExecutor, paths: Tuple[str, ...]) -> Set[str]:
        return {
            os.path.normpath(path)
            for path in collapse(
                wkr.map(
                    recurse,
                    chain.from_iterable(map(evaluate_glob, paths)),
                ),
                base_type=str,
            )
        }

    try:
        with ThreadPoolExecutor(max_workers=cpu_count()) as worker:
            all_paths = evaluate(worker, include) - evaluate(worker, exclude)

        nu_paths: Set[str] = get_non_upgradable_paths(all_paths)
        interm_paths: Set[str] = all_paths - nu_paths
        nv_paths: Set[str] = get_non_verifiable_paths(interm_paths)
        ok_paths: Set[str] = interm_paths - nv_paths

    except FileNotFoundError as exc:
        raise SystemExit(f"File does not exist: {exc.filename}") from exc
    else:
        log_blocking("info", "Files to be tested: %s", len(ok_paths))

    return Paths(
        ok_paths=tuple(ok_paths),
        nu_paths=tuple(nu_paths),
        nv_paths=tuple(nv_paths),
    )


def _iter_full_paths(path: str) -> Iterator[str]:
    """Recursively yield full paths to files for a given starting path."""
    if os.path.isfile(path):
        yield path
    elif os.path.exists(path):
        for entry in os.scandir(path):
            full_path = entry.path
            if entry.is_dir(follow_symlinks=False):
                yield f"{entry.path}/"
                yield from _iter_full_paths(full_path)
            else:
                yield full_path


def iter_rel_paths(starting_path: str) -> Iterator[str]:
    """Recursively yield relative paths to files for a given starting path."""
    yield from (
        path.replace(starting_path, "")[1:]
        for path in _iter_full_paths(starting_path)
    )
