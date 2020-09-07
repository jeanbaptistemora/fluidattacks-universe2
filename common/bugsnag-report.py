import bugsnag
import sys
import os

RELEASE_STAGE = os.environ['ENVIRONMENT_NAME']

BUGSNAG_API_KEYS = {
    'integrates_scheduler': '26294aec6a6dc262ee74b45d19aa7ec5',
}


def get_bugsnag_api_key(job_name):
    for job_prefix in sorted(BUGSNAG_API_KEYS.keys(), reverse=True):
        if job_name.startswith(job_prefix):
            return BUGSNAG_API_KEYS[job_prefix]

    return '13748c4b5f6807a89f327c0f54fe6c7a'  # ETL


def main(args):
    bugsnag.configure(
        api_key=get_bugsnag_api_key(args[1].lower()),
        release_stage=RELEASE_STAGE,
    )
    bugsnag.start_session()
    bugsnag.send_sessions()

    if args[0] == 'failed':
        raise Exception(f'Error with {" ".join(args[1:])}')


if __name__ == "__main__":
    main(sys.argv[1].split())
