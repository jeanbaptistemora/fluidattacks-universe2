# pylint: skip-file
from flask import (
    request,
    send_file,
    send_from_directory,
)
from typing import (
    Any,
)


def unsafe_file() -> None:
    file_at = request.args["file"]
    # Noncompliant
    send_file("static/%s" % file_at, as_attachment=True)


def safe_file(file_param: Any) -> None:
    file_at = request.args["file"]
    # Compliant: Using safe value
    send_from_directory("static", file_at)
    # Compliant: Not using user params
    send_file(file_param, as_attachment=True)
    # Compliant: Not sending as attachment
    send_file(file_at, as_attachment=False)
