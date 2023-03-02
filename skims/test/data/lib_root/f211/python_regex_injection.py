# pylint: skip-file
from flask import (
    request,
)
import os
import re


def unsafe_regex(mail: str) -> None:
    # Noncompliant: regex patterns built from user inputs
    username = request.args["username"]
    filename = str(request.files["attachment"].filename)
    re.search(username, filename)

    usermail = request.args["useremail"]
    re.match(usermail, mail)

    user_id = request.args["userId"]
    re.findall(user_id, os.environ["users"])


def safe_regex(mail: str) -> None:
    # Compliant: Regex pattern uses escaped user input
    username = re.escape(request.args["username"])
    filename = str(request.files["attachment"].filename)
    re.search(username, filename)

    usermail = request.args["useremail"]
    safe_patt = re.escape(usermail)
    re.match(safe_patt, mail)

    re.findall("[A-Z]*", filename)
