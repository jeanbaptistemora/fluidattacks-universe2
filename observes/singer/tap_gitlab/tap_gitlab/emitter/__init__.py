from dataclasses import (
    dataclass,
)
from tap_gitlab.api.client import (
    ApiClient,
)
from tap_gitlab.emitter.jobs import (
    JobStreamEmitter,
)
from tap_gitlab.emitter.mrs import (
    MrStreamEmitter,
)
from tap_gitlab.state import (
    factories,
    JobStreamState,
    MrStreamState,
)
from tap_gitlab.streams import (
    JobStream,
    MrStream,
)

fp_factory = factories.fp_factory
fp_factory_2 = factories.fp_factory_2


@dataclass(frozen=True)
class Emitter:
    client: ApiClient
    max_pages: int

    def emit_mrs(
        self, stream: MrStream, state: MrStreamState
    ) -> MrStreamState:
        mrs_emitter = MrStreamEmitter(self.client, stream, self.max_pages)
        f_progress = fp_factory.from_n_progress(
            state.state.process_until_incomplete(mrs_emitter.emit_interval, 0)
        )
        return MrStreamState(f_progress)

    def emit_jobs(
        self, stream: JobStream, state: JobStreamState
    ) -> JobStreamState:
        jobs_emitter = JobStreamEmitter(self.client, stream, self.max_pages)
        f_progress = fp_factory_2.from_n_progress(
            state.state.process_until_incomplete(jobs_emitter.emit_interval, 0)
        )
        return JobStreamState(f_progress)
