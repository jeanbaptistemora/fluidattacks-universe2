# SPDX-FileCopyrightText: 2022 "Fluid Attacks <development@fluidattacks.com>"
#
# SPDX-License-Identifier: MPL-2.0

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
    return _data.require_str("author_email").bind(
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
    )


def _decode_job_conf(data: JsonObj) -> ResultE[JobConf]:
    _data = JsonDecodeUtils(data)
    return _data.require_bool("allow_failure").bind(
        lambda allow_failure: _data.require_str("tag_list")
        .map(lambda tags: tuple(tags.split(",")))
        .bind(
            lambda tag_list: _data.require_str("ref_branch").bind(
                lambda ref_branch: _data.get_str("runner").bind(
                    lambda runner: _data.require_str("stage").map(
                        lambda stage: JobConf(
                            allow_failure, tag_list, ref_branch, runner, stage
                        )
                    )
                )
            )
        )
    )


def _decode_job_result(data: JsonObj) -> ResultE[JobResultStatus]:
    _data = JsonDecodeUtils(data)
    return _data.require_str("status").bind(
        lambda status: _data.get_str("failure_reason").bind(
            lambda failure_reason: _data.get_float("duration")
            .map(lambda m: m.map(Decimal))
            .bind(
                lambda duration: _data.get_float("queued_duration")
                .map(lambda m: m.map(Decimal))
                .bind(
                    lambda queued_duration: _data.require_int("user_id").map(
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


def _decode_job(data: JsonObj) -> ResultE[Job]:
    return _decode_commit(data).bind(
        lambda commit: _decode_job_dates(data).bind(
            lambda dates: _decode_job_conf(data).bind(
                lambda conf: _decode_job_result(data).map(
                    lambda result: Job(commit, dates, conf, result)
                )
            )
        )
    )


def decode_job_obj(data: JsonObj) -> ResultE[JobObj]:
    _data = JsonDecodeUtils(data)
    return (
        _data.require_int("id")
        .map(JobId)
        .bind(lambda jid: _decode_job(data).map(lambda j: JobObj(jid, j)))
    )
