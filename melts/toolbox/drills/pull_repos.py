# Standard libraries
import os
from typing import (
    List,
    Set,
)
import shutil
import urllib.parse

# Third party libraries
import pathspec

# Local libraries
from toolbox.drills import generic as drills_generic
from toolbox.utils.function import shield
from toolbox import (
    logger,
    utils,
)
from toolbox.utils.integrates import (
    get_filter_rules,
)


def notify_out_of_scope(
    repo_name: str,
    include_regexps: str,
    exclude_regexps: str,
) -> bool:
    logger.info(f'Please remember the scope for : {repo_name}')
    logger.info('  In scope:')
    for regex in include_regexps:
        logger.info(f'    - {regex}')

    if exclude_regexps:
        logger.info()
        logger.info('  Out of scope:')
        for regex in exclude_regexps:
            logger.info(f'    - {regex}')

    logger.info()

    return True


def get_repo_from_url(url: str) -> str:
    # Parse the URL
    url_obj = urllib.parse.urlparse(url)

    # Unquote the path portion, it may contain URL encoded characters
    url_path = urllib.parse.unquote_plus(url_obj.path)

    # Return the last component of the path
    repo = os.path.basename(url_path)

    # It may end with .git
    if repo.endswith('.git'):
        repo = repo[0:-4]

    return repo


def delete_out_of_scope_files(group: str) -> bool:
    # This entire function should be rewritten:
    #   https://gitlab.com/fluidattacks/product/-/issues/2617#note_474753627
    # I'm patching it for now (2020-12-28) so it survives a few days
    # The business logic is going to change when we all get to an agreement

    expected_repositories: Set[str] = set()
    path_to_fusion: str = os.path.join('groups', group, 'fusion')

    for root in get_filter_rules(group):
        # Get the expected repo name from the URL
        repo_name = get_repo_from_url(root['url'])
        expected_repositories.add(repo_name)

        spec_ignore = pathspec.PathSpec.from_lines('gitwildmatch',
                                                   root['filter']['exclude'])

        # Display to the user the Scope
        notify_out_of_scope(
            repo_name,
            root['filter']['include'],
            root['filter']['exclude'],
        )

        # Compute what files should be deleted according to the scope rules
        path_to_repo = os.path.join('groups', group, 'fusion', repo_name)
        for path in utils.file.iter_rel_paths(path_to_repo):
            if spec_ignore.match_file(path):
                path = os.path.join(path_to_fusion, repo_name, path)
                if os.path.isfile(path):
                    os.unlink(path)
                elif os.path.isdir(path):
                    os.removedirs(path)

    # Delete cloned repositories that are not expected to be cloned
    cloned_repositories: Set[str] = set(os.listdir(path_to_fusion))
    bad_repositories: Set[str] = cloned_repositories - expected_repositories

    if bad_repositories:
        logger.error('We cloned repositories that are not on Integrates')
        logger.error('This is very likely a bug, please notify the manager')
        for repository in bad_repositories:
            logger.warn(f'  Deleting, out of scope: {repository}')
            shutil.rmtree(os.path.join(path_to_fusion, repository))

    return True


def pull_repos_s3_to_fusion(subs: str,
                            local_path: str,
                            repository_name: str = 'all') -> bool:
    '''
    Download repos from s3 to a provided path

    param: subs: group to work with
    param: local_path: Path to store downloads
    '''

    if repository_name != 'all':
        local_path = f'{local_path}/{repository_name}'
    else:
        repository_name = ''

    bucket_path: str = f's3://continuous-repositories/' \
        f'{subs}/{repository_name}'

    os.makedirs(local_path, exist_ok=True)

    aws_sync_command: List[str] = [
        'aws', 's3', 'sync',
        '--delete',
        '--sse', 'AES256',
        '--exact-timestamps',
        bucket_path, local_path,
    ]

    git_expand_repositories_command: List[str] = [
        'find', local_path,
        '-name', '.git',
        '-execdir',
        'git', 'checkout',
        '--', '.', ';'
    ]
    logger.info(f'Downloading {subs} repositories')

    # Passing None to stdout and stderr shows the s3 progress
    # We want the CI to be as quiet as possible to have clean logs
    kwargs = dict() if utils.generic.is_env_ci() else dict(
        stdout=None,
        stderr=None,
    )

    status, stdout, stderr = utils.generic.run_command(
        cmd=aws_sync_command,
        cwd='.',
        env={},
        **kwargs,
    )

    if status:
        logger.error('Sync from bucket has failed:')
        logger.info(stdout)
        logger.info(stderr)
        logger.info()
        return False

    git_status, git_stdout, git_stderr = utils.generic.run_command(
        cmd=git_expand_repositories_command,
        cwd='.',
        env={},
        **kwargs,
    )

    if git_status:
        logger.error('Expand repositories has failed:')
        logger.info(git_stdout)
        logger.info(git_stderr)
        logger.info()
        return False
    return True


@shield(retries=1)
def main(subs: str, repository_name: str = 'all') -> bool:
    '''
    Clone all repos for a group

    param: subs: group to work with
    '''
    bucket: str = 'continuous-repositories'
    passed: bool = True
    if not utils.generic.does_subs_exist(subs):
        logger.error(f'group {subs} does not exist.')
        passed = False
        return passed

    utils.generic.aws_login(f'continuous-{subs}')

    if not drills_generic.s3_path_exists(bucket, f'{subs}/'):
        logger.error(f'group {subs} does not have repos uploaded to s3')
        passed = False
    else:
        local_path: str = f'groups/{subs}/fusion/'

        logger.info('Computing last upload date')
        days: int = \
            drills_generic.calculate_days_ago(
                drills_generic.get_last_upload(bucket, f'{subs}/'))

        passed = passed \
            and pull_repos_s3_to_fusion(subs, local_path, repository_name) \
            and delete_out_of_scope_files(subs)

        logger.info(f'Data for {subs} was uploaded to S3 {days} days ago')

    return passed
