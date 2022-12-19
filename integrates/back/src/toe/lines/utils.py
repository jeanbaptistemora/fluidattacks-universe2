from os import (
    path,
)


def get_filename_extension(filename: str) -> str:
    _, extension = path.splitext(filename)
    return extension.removeprefix(".").lower()
