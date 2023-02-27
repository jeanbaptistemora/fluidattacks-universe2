# pylint: skip-file
from flask import (
    request,
)
import os
import shlex
import subprocess


def unsafe_command() -> None:
    address = request.args.get("address")
    cmd = "ping -c 1 %s" % address
    # Noncompliant
    os.popen(cmd)
    # Noncompliant; using shell=true is unsafe
    subprocess.Popen(cmd, shell=True)


def safe_command(param: str) -> None:
    # Escape distinguished names special characters
    address = shlex.quote(request.args["address"])
    cmd = "ping -c 1 %s" % address
    # Compliant: Escaped user params
    os.popen(cmd)
    # Compliant: Do not execute user params
    os.popen(param)
    # Compliant, shell= False by default
    subprocess.Popen(cmd)
