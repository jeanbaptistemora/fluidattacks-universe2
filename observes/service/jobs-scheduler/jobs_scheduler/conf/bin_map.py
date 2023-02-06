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
    if job is Job.DELIGHTED:
        return os.environ["delightedEtl"]
    if job is Job.DYNAMO_INTEGRATES_MAIN:
        return f'{os.environ["dynamoDbEtls"]} CORE'
    if job is Job.DYNAMO_INTEGRATES_MAIN_NO_CACHE:
        return f'{os.environ["dynamoDbEtls"]} DETERMINE_SCHEMA'
    if job is Job.FORMSTACK:
        return os.environ["formstackEtl"]
    if job is Job.GITLAB_PRODUCT:
        return os.environ["gitlabEtlProduct"]
    if job is Job.MAILCHIMP_ETL:
        return os.environ["mailchimpEtl"]
    if job is Job.MANDRILL_ETL:
        return os.environ["mandrillEtl"]
    if job is Job.MIRROR:
        return os.environ["codeEtlMirror"]
    if job is Job.UPLOAD:
        return os.environ["codeEtlUpload"]
