from decimal import (
    Decimal,
)
from fa_purity import (
    JsonObj,
    ResultE,
)
from tap_gitlab.api2._utils import (
    JsonDecodeUtils,
    str_to_datetime,
)
from tap_gitlab.api2.job import (
    Commit,
    Job,
    JobConf,
    JobDates,
    JobId,
    JobObj,
    JobResultStatus,
)


def _decode_commit(data: JsonObj) -> ResultE[Commit]:
    _data = JsonDecodeUtils(data)
    created_at = _data.require_str("created_at").bind(str_to_datetime)
    return (
        _data.require_str("author_email")
        .bind(
            lambda email: _data.require_str("author_name").bind(
                lambda name: _data.require_str("id").bind(
                    lambda hash_id: _data.require_str("message").bind(
                        lambda message: _data.require_str("short_id").bind(
                            lambda short_id: _data.require_str("title").bind(
                                lambda title: created_at.map(
                                    lambda created: Commit(
                                        email,
                                        name,
                                        created,
                                        hash_id,
                                        message,
                                        short_id,
                                        title,
                                    )
                                )
                            )
                        )
                    )
                )
            )
        )
        .alt(lambda e: Exception(f"Cannot decode job commit. sub-error: {e}"))
    )


def _decode_job_dates(data: JsonObj) -> ResultE[JobDates]:
    _data = JsonDecodeUtils(data)
    return (
        _data.require_str("created_at")
        .bind(str_to_datetime)
        .bind(
            lambda created_at: _data.get_datetime("started_at").bind(
                lambda started_at: _data.get_datetime("finished_at").map(
                    lambda finished_at: JobDates(
                        created_at, started_at, finished_at
                    )
                )
            )
        )
    ).alt(lambda e: Exception(f"Cannot decode job dates. sub-error: {e}"))


def _decode_job_conf(data: JsonObj) -> ResultE[JobConf]:
    _data = JsonDecodeUtils(data)
    return (
        _data.require_bool("allow_failure")
        .bind(
            lambda allow_failure: _data.require_list_of_str("tag_list").bind(
                lambda tag_list: _data.require_str("ref").bind(
                    lambda ref_branch: _data.require_str("stage").map(
                        lambda stage: JobConf(
                            allow_failure,
                            tag_list,
                            ref_branch,
                            stage,
                        )
                    )
                )
            )
        )
        .alt(lambda e: Exception(f"Cannot decode job conf. sub-error: {e}"))
    )


def _decode_job_result(data: JsonObj) -> ResultE[JobResultStatus]:
    _data = JsonDecodeUtils(data)
    return (
        _data.require_str("status")
        .bind(
            lambda status: _data.get_str("failure_reason").bind(
                lambda failure_reason: _data.get_float("duration")
                .map(lambda m: m.map(Decimal))
                .bind(
                    lambda duration: _data.get_float("queued_duration")
                    .map(lambda m: m.map(Decimal))
                    .bind(
                        lambda queued_duration: _data.require_json(
                            "user"
                        ).bind(
                            lambda user: JsonDecodeUtils(user)
                            .require_int("id")
                            .map(
                                lambda user_id: JobResultStatus(
                                    status,
                                    failure_reason,
                                    duration,
                                    queued_duration,
                                    user_id,
                                )
                            )
                        )
                    )
                )
            )
        )
        .alt(lambda e: Exception(f"Cannot decode job result. sub-error: {e}"))
    )


def _decode_job(data: JsonObj) -> ResultE[Job]:
    _data = JsonDecodeUtils(data)
    return (
        _data.require_json("commit")
        .bind(_decode_commit)
        .bind(
            lambda commit: _decode_job_dates(data).bind(
                lambda dates: _decode_job_conf(data).bind(
                    lambda conf: _decode_job_result(data).map(
                        lambda result: Job(commit, dates, conf, result)
                    )
                )
            )
        )
        .alt(lambda e: Exception(f"Cannot decode job. sub-error: {e}"))
    )


def decode_job_id(data: JsonObj) -> ResultE[JobId]:
    return (
        JsonDecodeUtils(data)
        .require_int("id")
        .map(JobId)
        .alt(lambda e: Exception(f"Cannot decode job id. sub-error: {e}"))
    )


def decode_job_obj(data: JsonObj) -> ResultE[JobObj]:
    _id = decode_job_id(data)
    return _id.bind(
        lambda jid: _decode_job(data).map(lambda j: JobObj(jid, j))
    ).alt(lambda e: Exception(f"Cannot decode job obj. sub-error: {e}"))
