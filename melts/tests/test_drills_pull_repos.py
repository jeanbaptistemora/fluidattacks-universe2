# Standard libraries
from shutil import rmtree

# Local libraries
from toolbox.drills import pull_repos

EXISTING_REPO: str = 'continuoustest'
EXISTING_REPO_NO_PERMISSIONS: str = 'daimon'
NON_EXISTING_REPO: str = 'sodjfoisajfdoiasjfdoia'
LOCAL_PATH = 'continuoustest'


def test_drills_pull_repos():
    try:
        assert pull_repos.pull_repos_s3_to_fusion(EXISTING_REPO, LOCAL_PATH)
        assert not pull_repos.main(EXISTING_REPO_NO_PERMISSIONS)
        assert not pull_repos.main(NON_EXISTING_REPO)
    finally:
        rmtree(LOCAL_PATH)


def test_get_repo_from_url() -> None:
    for url, repo in (
        (
            'ssh://git@gitlab.com:fluidattacks/product.git',
            'product',
        ),
        (
            'ssh://git@vs-ssh.visualstudio.com:v3/grupo/something Tecnología/Test',
            'Test',
        ),
        (
            'ssh://git@vs-ssh.visualstudio.com:v3/grupo/something+Tecnolog%C3%ADa/Test+test',
            'Test test',
        ),
    ):
        assert pull_repos.get_repo_from_url(url) == repo
