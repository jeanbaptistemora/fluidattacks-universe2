from __future__ import (
    annotations,
)

from .._core import (
    JobState,
    MaxRetriesReached,
)
from fa_purity import (
    Cmd,
    FrozenList,
    Result,
    ResultE,
)
from fa_purity.cmd.core import (
    CmdUnwrapper,
    new_cmd,
)
from fa_purity.pure_iter import (
    factory as PIterFactory,
)
from fa_purity.utils import (
    raise_exception,
)
import logging
from tap_mandrill._files import (
    BinFile,
    StrFile,
    ZipFile,
)
from tap_mandrill.api.export._core import (
    ExportJob,
)
from time import (
    sleep,
)
from typing import (
    Union,
)

LOG = logging.getLogger(__name__)


def download(job: ExportJob) -> Cmd[ResultE[StrFile]]:
    return (
        BinFile.from_url(job.result_url.unwrap())
        .map(lambda r: r.alt(raise_exception).unwrap())
        .map(ZipFile.from_bin)
        .bind(
            lambda r: r.map(
                lambda z: z.extract_single_file().map(
                    lambda x: Result.success(x, Exception)
                )
            )
            .alt(lambda x: Cmd.from_cmd(lambda: Result.failure(x, StrFile)))
            .to_union()
        )
    )


def until_finish(
    get_jobs: Cmd[FrozenList[ExportJob]],
    job: ExportJob,
    check_interval: int,
    max_retries: int,
) -> Cmd[Result[ExportJob, Union[MaxRetriesReached, KeyError]]]:
    def _action(
        act: CmdUnwrapper,
    ) -> Result[ExportJob, Union[MaxRetriesReached, KeyError]]:
        retry_num = max_retries + 1
        while retry_num > 0:
            LOG.info("Consulting status of: %s", job.job_id)
            jobs = PIterFactory.from_flist(act.unwrap(get_jobs))
            updated_job = jobs.find_first(lambda j: j.job_id == job.job_id)
            state = updated_job.map(lambda j: j.state)
            in_progress = state.map(
                lambda s: s in (JobState.waiting, JobState.working)
            ).value_or(False)
            if in_progress:
                LOG.info("Job %s not finished, waiting...", job.job_id)
                retry_num = retry_num - 1
                sleep(check_interval)
            else:
                if updated_job.value_or(None):
                    LOG.info("Job %s completed", job.job_id)
                return updated_job.to_result().alt(
                    lambda _: KeyError(f"Missing job {job.job_id}")
                )
        err = MaxRetriesReached(f"Waiting for job {job.job_id}")
        return Result.failure(err, ExportJob)

    return new_cmd(_action)
