# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from __future__ import (
    annotations,
)

from ._bin_file import (
    BinFile,
)
from ._str_file import (
    StrFile,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
    Result,
    ResultE,
)
from fa_purity.cmd import (
    unsafe_unwrap,
)
from pathlib import (
    Path,
)
from tempfile import (
    TemporaryDirectory,
)
from typing import (
    Callable,
    IO,
    TypeVar,
)
from zipfile import (
    BadZipFile,
    LargeZipFile,
    ZipFile as _BaseZipFile,
)

_T = TypeVar("_T")


@dataclass(frozen=True)
class _ZipFile:
    file: BinFile


@dataclass(frozen=True)
class ZipFile:
    _inner: _ZipFile

    @staticmethod
    def from_bin(bin_file: BinFile) -> ResultE[ZipFile]:
        builder = bin_file.unsafe_transform(lambda f: _BaseZipFile(f, "r"))
        try:
            # semanticly all _BaseZipFile objs produced by the builder are equivalent,
            # since BinFile is supposed immutable, but its mutable state is independent
            with unsafe_unwrap(builder):
                # test _BaseZipFile build success
                pass
            return Result.success(ZipFile(_ZipFile(bin_file)), Exception)
        except (BadZipFile, LargeZipFile) as err:
            return Result.failure(err)

    def _unsafe_map(self, function: Callable[[_BaseZipFile], _T]) -> Cmd[_T]:
        def _action(file: IO[bytes]) -> Cmd[_T]:
            def _inner() -> _T:
                with _BaseZipFile(file.name, "r") as zip_obj:
                    return function(zip_obj)

            return Cmd.from_cmd(_inner)

        return self._inner.file.unsafe_transform(_action).bind(lambda x: x)

    def _extract_single(self, target_dir: Path) -> Cmd[Path]:
        def _extract(zip_obj: _BaseZipFile) -> Path:
            files = zip_obj.namelist()
            if len(files) != 1:
                raise Exception(
                    f"Expected only 1 compressed file got {len(files)}"
                )
            path = zip_obj.extract(files[0], target_dir.as_posix())
            return Path(path)

        return self._unsafe_map(_extract)

    def extract_single_file(self) -> Cmd[StrFile]:
        def _action() -> Cmd[StrFile]:
            with TemporaryDirectory() as dir:
                dir_path = Path(dir)
                return self._extract_single(dir_path).bind(StrFile.freeze)

        return Cmd.from_cmd(_action).bind(lambda x: x)
