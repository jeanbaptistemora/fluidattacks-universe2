# Standard library
from datetime import (
    datetime,
)
from itertools import (
    chain,
)

# Third party libraries
import boto3
import bugsnag

# Constants
HOUR: float = 3600.0
NOW: float = datetime.utcnow().timestamp()

# Side effects
bugsnag.configure(
    api_key='13748c4b5f6807a89f327c0f54fe6c7a',
    asynchronous=False,
    send_code=False,
)


class BatchSucceededJob(Exception):
    pass


class BatchFailedJob(Exception):
    pass


def report_msg(
    container: str,
    identifier: str,
    name: str,
    reason: str,
    success: bool,
) -> None:
    arguments = dict(
        exception=(BatchSucceededJob if success else BatchFailedJob)(name),
        extra=dict(
            container=container,
            identifier=identifier,
            reason=reason,
        ),
        grouping_hash=name,
    )

    print(arguments)
    bugsnag.start_session()
    bugsnag.notify(**arguments)
    bugsnag.send_sessions()


def main() -> None:
    client = boto3.client('batch')
    paginator = client.get_paginator('list_jobs')

    for items in chain(
        paginator.paginate(
            jobQueue='default',
            jobStatus='SUCCEEDED',
        ),
        paginator.paginate(
            jobQueue='default',
            jobStatus='FAILED',
        ),
    ):
        for job in items['jobSummaryList']:
            # Timestamps from aws come in miliseconds
            created_at: float = job['createdAt'] / 1000

            if created_at > NOW - 24 * HOUR:
                report_msg(
                    container=str(job.get('container')),
                    identifier=job['jobId'],
                    name=job['jobName'],
                    reason=job['statusReason'],
                    success=job['status'] == 'SUCCEEDED',
                )


if __name__ == '__main__':
    main()
