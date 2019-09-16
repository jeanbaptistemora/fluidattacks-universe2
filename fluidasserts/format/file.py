# -*- coding: utf-8 -*-

"""This module allows to check common ``file`` vulnerabilities."""


# standard imports
from typing import List
from os.path import splitext, basename

# 3rd party imports
import magic

# local imports
from fluidasserts import Unit, SAST, LOW, CLOSED, OPEN
from fluidasserts.utils.generic import get_paths, get_sha256
from fluidasserts.utils.decorators import api, unknown_if


COMPILED_BINARY_MIMES: List[str] = [
    'application/java-archive',
    'application/x-java-applet',
]


@api(risk=LOW, kind=SAST)
@unknown_if(FileNotFoundError)
def has_compiled_binaries(path: str,
                          mime_types: List[str] = COMPILED_BINARY_MIMES.copy(),
                          exclude: List[str] = None) -> tuple:
    """
    Check if there are files in *path* that match a compiled binary mime type.

    Check if the source code of the binaries found is available

    It checks for `fluidasserts.format.file.COMPILED_BINARY_MIMES`
    mime types.

    :param path: location to check recursively
    :param mime_types: List of mime types to consider vulnerable
    :param exclude: Paths that contains any string from this list are ignored.
    :rtype: :class:`fluidasserts.Result`
    """
    msg_open: str = 'File is a compiled binary'
    msg_closed: str = 'File is not a compiled binary'

    safes: List[Unit] = []
    vulns: List[Unit] = []

    exclude = exclude or tuple()

    paths = get_paths(path, exclude=tuple(exclude))
    for file in paths:
        mime_type: str = magic.from_file(file, mime=True)

        vulnerable: bool = mime_type in mime_types
        if vulnerable:
            filename = splitext(basename(file))[0]
            filename = filename.split('$')[0]
            filename += '.java'
            source_exists = any(i.endswith(filename) for i in paths)

        (vulns if vulnerable and not source_exists else safes).append(
            Unit(where=file,
                 source='FILE/MimeType/Binary',
                 specific=[msg_open if vulnerable else msg_closed],
                 fingerprint=get_sha256(file)))

    if vulns:
        return OPEN, msg_open, vulns, safes
    return CLOSED, msg_closed, vulns, safes
