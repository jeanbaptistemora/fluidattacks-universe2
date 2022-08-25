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
from zipfile import (
    BadZipFile,
    LargeZipFile,
    ZipFile as _BaseZipFile,
)


@dataclass(frozen=True)
class _ZipFile:
    file: Cmd[_BaseZipFile]


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
            return Result.success(ZipFile(_ZipFile(builder)), Exception)
        except (BadZipFile, LargeZipFile) as err:
            return Result.failure(err)

    def _extract_single(self, target_dir: Path) -> Cmd[Path]:
        def _extract(zip_obj: _BaseZipFile) -> Cmd[Path]:
            files = zip_obj.namelist()
            if len(files) > 1:
                raise Exception(
                    f"Expected only 1 compressed file got {len(files)}"
                )
            return Cmd.from_cmd(
                lambda: zip_obj.extract(files[0], target_dir.as_posix())
            ).map(lambda p: Path(p))

        return self._inner.file.bind(lambda z: _extract(z))

    def extract_single_file(self) -> Cmd[StrFile]:
        def _action() -> Cmd[StrFile]:
            with TemporaryDirectory() as dir:
                dir_path = Path(dir)
                return self._extract_single(dir_path).bind(StrFile.freeze)

        return Cmd.from_cmd(_action).bind(lambda x: x)
