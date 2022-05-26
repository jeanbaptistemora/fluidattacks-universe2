from enum import (
    Enum,
)
from fa_purity import (
    Cmd,
)
import sys
from tap_gitlab.api2._raw import (
    Credentials,
    RawClient,
)
from tap_gitlab.api2.issues import (
    IssueClient,
)
from tap_gitlab.streamer import (
    Streamer,
)


class Streams(Enum):
    ISSUES = "ISSUES"


def project_stream(api_key: str, project: str, stream: str) -> Cmd[None]:
    _stream = Streams(stream.upper())
    _project = int(project)
    raw = RawClient(Credentials(api_key))
    streamer = Streamer(sys.stdout)
    if _stream is Streams.ISSUES:
        return streamer.issues(IssueClient(raw, None), _project)
