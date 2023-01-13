import boto3
import bugsnag
from cryptography.fernet import (
    Fernet,
)
import logging
from multiprocessing import (
    Manager,
)
from multiprocessing.managers import (
    SyncManager,
)
from os import (
    environ,
)
import re
from typing import (
    Any,
)

# This CTX will store constants that we need to
# be cross-threaded, just user API_TOKEN for now
MANAGER: SyncManager = Manager()
CTX: Any = MANAGER.Namespace()

STATIC_DIR: str = environ["SORTS_STATIC_PATH"]

STAT_REGEX: re.Pattern = re.compile(
    r"([0-9]+ files? changed)?"
    r"(, (?P<insertions>[0-9]+) insertions \(\+\))?"
    r"(, (?P<deletions>[0-9]+) deletions \(\-\))?"
)
RENAME_REGEX: re.Pattern = re.compile(
    r"(?P<pre_path>.*)?"
    r"{(?P<old_name>.*) => (?P<new_name>.*)}"
    r"(?P<post_path>.*)?"
)

# Logging
LOGGER_HANDLER: logging.StreamHandler = logging.StreamHandler()
LOGGER: logging.Logger = logging.getLogger("Sorts")
LOGGER_REMOTE_HANDLER = bugsnag.handlers.BugsnagHandler()
LOGGER_REMOTE: logging.Logger = logging.getLogger("Sorts.stability")

# Encryption
FERNET = Fernet(
    environ.get("FERNET_TOKEN", Fernet.generate_key())  # type: ignore
)

# AWS-related
S3_BUCKET_NAME: str = "sorts"
S3_RESOURCE = boto3.resource("s3")
S3_BUCKET = S3_RESOURCE.Bucket(S3_BUCKET_NAME)
