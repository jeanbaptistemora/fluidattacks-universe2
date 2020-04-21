# Local libraries
from toolbox.drills import pull_repos

EXISTING_REPO: str = 'continuoustest'
EXISTING_REPO_NO_PERMISSIONS: str = 'daimon'
NON_EXISTING_REPO: str = 'sodjfoisajfdoiasjfdoia'
LOCAL_PATH = 'continuoustest2'

def test_drills_pull_repos():
    assert pull_repos.pull_repos_s3_to_fusion(EXISTING_REPO, LOCAL_PATH)
    assert not pull_repos.main(EXISTING_REPO_NO_PERMISSIONS)
    assert not pull_repos.main(NON_EXISTING_REPO)
