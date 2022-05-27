from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
)
from fa_purity.stream.transform import (
    chain,
    consume,
)
from fa_singer_io.singer import (
    emitter,
)
from tap_gitlab.api2.ids import (
    ProjectId,
)
from tap_gitlab.api2.issues import (
    IssueClient,
)
from tap_gitlab.singer.issues import (
    records as issue_record,
)
from typing import (
    IO,
)


@dataclass(frozen=True)
class Streamer:
    _target: IO[str]

    def issues(self, client: IssueClient, project: ProjectId) -> Cmd[None]:
        return (
            client.project_issues(project)
            .map(issue_record.issue_records)
            .transform(lambda x: chain(x))
            .map(lambda s: emitter.emit(self._target, s))
            .transform(lambda x: consume(x))
        )
