# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from jobs_scheduler.conf.job import (
    Job,
)
import os
from typing import (
    NoReturn,
)


def job_to_bin_cmd(job: Job) -> str | NoReturn:
    if job is Job.ANNOUNCEKIT:
        return os.environ["announceKitEtl"]
    if job is Job.BUGSNAG:
        return os.environ["bugsnagEtl"]
    if job is Job.CHECKLY:
        return os.environ["checklyEtl"]
    if job is Job.CHECKLY_LEGACY:
        return os.environ["checklyEtlLegacy"]
    if job is Job.DELIGHTED:
        return os.environ["delightedEtl"]
    if job is Job.DYNAMO_FORCES:
        return f'{os.environ["dynamoDbEtls"]} FORCES'
    if job is Job.DYNAMO_INTEGRATES:
        return f'{os.environ["dynamoDbEtls"]} GROUP'
    if job is Job.DYNAMO_INTEGRATES_MAIN:
        return f'{os.environ["dynamoDbEtls"]} CORE'
    if job is Job.DYNAMO_INTEGRATES_MAIN_NO_CACHE:
        return f'{os.environ["dynamoDbEtls"]} CORE_NO_CACHE'
    if job is Job.FORMSTACK:
        return os.environ["formstackEtl"]
    if job is Job.GITLAB_PRODUCT:
        return os.environ["gitlabEtlProduct"]
    if job is Job.GITLAB_CHALLENGES:
        return os.environ["gitlabEtlChallenges"]
    if job is Job.GITLAB_DEFAULT:
        return os.environ["gitlabEtlDefault"]
    if job is Job.GITLAB_SERVICES:
        return os.environ["gitlabEtlServices"]
    if job is Job.MAILCHIMP_ETL:
        return os.environ["mailchimpEtl"]
    if job is Job.MANDRILL_ETL:
        return os.environ["mandrillEtl"]
    if job is Job.MIRROR:
        return os.environ["codeEtlMirror"]
    if job is Job.REPORT_FAILS:
        return os.environ["batchStability"] + " report-failures observes"
    if job is Job.REPORT_CANCELLED:
        return os.environ["batchStability"] + " report-cancelled observes"
    if job is Job.UPLOAD:
        return os.environ["codeEtlUpload"]
