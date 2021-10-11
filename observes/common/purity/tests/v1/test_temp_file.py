from purity.v1 import (
    OpenStrFile,
    TempFile,
)
from returns.io import (
    IO,
)


def test_temp_file() -> None:
    msg = "Hello World!"

    def mock_write(file: OpenStrFile) -> IO[None]:
        file.write(msg)
        return IO(None)

    def mock_read(file: OpenStrFile) -> IO[str]:
        return IO(file.readline())

    f = TempFile("UTF-8")
    f.map(mock_write, "w")
    msg2 = f.map(mock_read, "r")
    assert IO(msg) == msg2
