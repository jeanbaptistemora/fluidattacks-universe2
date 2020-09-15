import bugsnag
import sys
import os

RELEASE_STAGE = os.environ['ENVIRONMENT_NAME']
JOB_ID = os.environ.get('CI_JOB_ID', 'LOCAL')
ARGV = sys.argv[1].split()

BUGSNAG_API_KEYS = {
    'integrates_scheduler': '26294aec6a6dc262ee74b45d19aa7ec5',
}


def get_bugsnag_api_key(job_name):
    for job_prefix in sorted(BUGSNAG_API_KEYS.keys(), reverse=True):
        if job_name.startswith(job_prefix):
            return BUGSNAG_API_KEYS[job_prefix]

    return '13748c4b5f6807a89f327c0f54fe6c7a'  # ETL


def main():
    if RELEASE_STAGE == 'production':
        bugsnag.configure_request(
            meta_data={
                'JOB_INFO': {
                    'ENVIRONMENT': RELEASE_STAGE,
                    'CI_JOB_ID': JOB_ID,
                    'JOB_NAME': ARGV[1],
                    'PARAMATERS': ARGV[2:],
                    'JOB_COMPLETE': ' '.join(ARGV[1:]),
                },
            },
        )
        bugsnag.configure(
            api_key=get_bugsnag_api_key(ARGV[1].lower()),
            release_stage=RELEASE_STAGE,
        )
        bugsnag.start_session()
        bugsnag.send_sessions()

    if ARGV[0] == 'failed':
        raise Exception(
            f'Error with {" ".join(ARGV[1:])} | CI_JOB_ID: {JOB_ID}'
        )


if __name__ == "__main__":
    main()
