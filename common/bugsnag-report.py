import bugsnag
import sys

args = sys.argv[1].split()

bugsnag.configure(
    api_key='13748c4b5f6807a89f327c0f54fe6c7a',
    release_stage=args[0],
)
bugsnag.start_session()
bugsnag.send_sessions()

if len(args) > 1:
    raise Exception(f'Error with {" ".join(args[1:])}')
