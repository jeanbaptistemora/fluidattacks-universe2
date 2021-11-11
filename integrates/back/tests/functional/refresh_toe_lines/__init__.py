from _pytest.monkeypatch import (
    MonkeyPatch,
)
from back.tests.functional.utils import (
    get_batch_job,
    get_graphql_result,
)
from batch import (
    dispatch,
    toe_lines,
)
from dataloaders import (
    get_new_context,
)
import glob
import os
import shutil
import sys
from typing import (
    Any,
    Dict,
)


async def get_result(
    *,
    user: str,
    group_name: str,
    monkeypatch: MonkeyPatch,
) -> Dict[str, Any]:
    def mocked_pull_repositories(
        tmpdir: str, group_name: str, repo_nickname: str
    ) -> None:
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, "mocks")
        fusion_path = f"{tmpdir}/groups/{group_name}/fusion"
        if repo_nickname:
            shutil.copytree(
                f"{filename}/{repo_nickname}", f"{fusion_path}/{repo_nickname}"
            )
        else:
            shutil.copytree(filename, fusion_path)

        git_mocks = glob.glob(f"{fusion_path}/*/.git_mock")
        for git_mock in git_mocks:
            os.rename(git_mock, git_mock.replace("/.git_mock", "/.git"))

    query: str = f"""
        mutation {{
            refreshToeLines(
                groupName: "{group_name}",
            ) {{
                success
            }}
        }}
    """
    data: Dict[str, Any] = {"query": query}
    result = await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
    if result["data"]:
        batch_action = await get_batch_job(entity=group_name)
        monkeypatch.setattr(
            sys,
            "argv",
            [
                "test",
                batch_action.action_name,
                batch_action.subject,
                batch_action.entity,
                batch_action.time,
                batch_action.additional_info,
            ],
        )
        monkeypatch.setattr(
            toe_lines,
            "pull_repositories",
            mocked_pull_repositories,
        )
        await dispatch.main()
    return result


async def query_get(
    *,
    user: str,
    group_name: str,
) -> Dict[str, Any]:
    query: str = f"""{{
        group(groupName: "{group_name}"){{
            name
            roots {{
                ... on GitRoot {{
                    id
                    toeLines {{
                        attackedAt
                        attackedBy
                        attackedLines
                        bePresent
                        bePresentUntil
                        comments
                        commitAuthor
                        filename
                        firstAttackAt
                        loc
                        modifiedCommit
                        modifiedDate
                        seenAt
                        sortsRiskLevel
                    }}
                }}
            }}
        }}
      }}
    """
    data: Dict[str, Any] = {"query": query}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
