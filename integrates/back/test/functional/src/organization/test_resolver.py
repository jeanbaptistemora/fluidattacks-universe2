# pylint: disable=too-many-statements, import-error
from . import (
    get_result,
    get_vulnerabilities_url,
)
from azure.devops.v6_0.git.models import (
    GitCommit,
    GitRepository,
    GitRepositoryStats,
    GitUserDate,
    TeamProjectReference,
)
from back.test.functional.src.remove_credentials import (
    get_result as remove_credentials,
)
from back.test.functional.src.remove_stakeholder_access import (
    get_access_token,
)
from custom_exceptions import (
    RequiredVerificationCode,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
    timedelta,
)
from db_model.azure_repositories.types import (
    BasicRepoData,
    CredentialsGitRepository,
)
from db_model.integration_repositories.types import (
    OrganizationIntegrationRepository,
)
from db_model.roots.types import (
    GitRoot,
)
from github import (
    GitCommit as GitHubCommit,
)
import glob
from newutils.datetime import (
    get_as_utc_iso_format,
    get_now_minus_delta,
)
import os
import pytest
from schedulers.update_organization_overview import (
    main as update_organization_overview,
)
from schedulers.update_organization_repositories import (
    main as update_organization_repositories,
)
import shutil
from typing import (
    Any,
    Optional,
)
from unittest import (
    mock,
)


def get_repositories(
    *, base_url: str, access_token: str  # pylint: disable=unused-argument
) -> tuple[GitRepository, ...]:
    return tuple(
        [
            GitRepository(
                project=TeamProjectReference(
                    last_update_time=get_now_minus_delta(days=2),
                    name="testprojects",
                ),
                default_branch="refs/head/main",
                id="2",
                remote_url=(
                    "ssh://git@test.com:v3/testprojects/_git/secondrepor"
                ),
                ssh_url="ssh://git@test.com:v3/testprojects/_git/secondrepor",
                url="ssh://git@test.com:v3/testprojects/_git/secondrepor",
                web_url="ssh://git@test.com:v3/testprojects/_git/secondrepor",
            ),
            GitRepository(
                project=TeamProjectReference(
                    last_update_time=get_now_minus_delta(days=2),
                    name="testprojects",
                ),
                default_branch="refs/head/trunk",
                id="1",
                remote_url="ssh://git@test.com:v3/testprojects/_git/firstrepo",
                ssh_url="ssh://git@test.com:v3/testprojects/_git/firstrepo",
                url="ssh://git@test.com:v3/testprojects/_git/firstrepo",
                web_url="ssh://git@test.com:v3/testprojects/_git/firstrepo",
            ),
        ]
    )


def get_repositories_commits(
    *,
    organization: str,  # pylint: disable=unused-argument
    access_token: str,  # pylint: disable=unused-argument
    repository_id: str,  # pylint: disable=unused-argument
    project_name: str,  # pylint: disable=unused-argument
) -> tuple[GitCommit, ...]:

    return tuple(
        [
            GitCommit(committer=GitUserDate(date=get_now_minus_delta(days=1))),
            GitCommit(committer=GitUserDate(date=get_now_minus_delta(days=2))),
        ]
    )


def get_repositories_stats(
    *,
    organization: str,  # pylint: disable=unused-argument
    access_token: str,  # pylint: disable=unused-argument
    repository_id: str,
    project_name: str,
) -> GitRepositoryStats:
    return GitRepositoryStats(
        branches_count=1,
        commits_count=5,
        repository_id=f"{project_name}/{repository_id}",
    )


def get_lab_repositories_stats(
    token: str,  # pylint: disable=unused-argument
) -> tuple[BasicRepoData, ...]:
    return tuple(
        [
            BasicRepoData(
                id="123456789",
                remote_url="ssh://git@test.com/testprojects/fourthtrepo",
                ssh_url="https://git@test.com/testprojects/fourthtrepo.git",
                web_url="https://test.com/testprojects/fourthtrepo",
                branch="refs/heads/main",
                last_activity_at=get_now_minus_delta(days=4),
            )
        ]
    )


def get_hub_repositories_stats(
    token: str,  # pylint: disable=unused-argument
) -> tuple[BasicRepoData, ...]:
    return tuple(
        [
            BasicRepoData(
                id="234567890",
                remote_url="ssh://git@test.com/testprojects/fifthtrepo",
                ssh_url="https://git@test.com/testprojects/fifthtrepo.git",
                web_url="https://test.com/testprojects/fifthtrepo",
                branch="refs/heads/dev",
                last_activity_at=get_now_minus_delta(days=6),
            )
        ]
    )


def get_lab_commit_stats(
    token: str,  # pylint: disable=unused-argument
    project_id: str,  # pylint: disable=unused-argument
) -> tuple[dict, ...]:
    return tuple(
        [
            dict(
                committed_date=get_as_utc_iso_format(
                    get_now_minus_delta(days=5)
                ),
                author_email="testemail1@test.test",
            ),
            dict(
                committed_date=get_as_utc_iso_format(
                    get_now_minus_delta(days=4)
                ),
                author_email="testemail2@test.test",
            ),
        ]
    )


def get_hub_commit_stats(
    token: str,  # pylint: disable=unused-argument
    repo_id: str,  # pylint: disable=unused-argument
) -> tuple[GitHubCommit.GitCommit, ...]:
    return tuple()


async def get_covered_group(
    path: str,  # pylint: disable=unused-argument
    folder: str,  # pylint: disable=unused-argument
    group: str,  # pylint: disable=unused-argument
    git_roots: tuple[GitRoot, ...],  # pylint: disable=unused-argument
) -> tuple[int, set[str]]:
    return (4, {"devtest1@test.com"})


async def _get_missed_authors(
    *,
    loaders: Dataloaders,  # pylint: disable=unused-argument
    repository: CredentialsGitRepository,  # pylint: disable=unused-argument
) -> set[str]:
    return {"devtest2@test.com"}


def mocked_pull_repositories(
    tmpdir: str, group_name: str, optional_repo_nickname: str
) -> None:
    dirname = os.path.dirname(__file__)
    filename = os.path.join(f"{dirname}/../refresh_toe_lines", "mocks")
    fusion_path = f"{tmpdir}/groups/{group_name}/fusion"
    if optional_repo_nickname:
        shutil.copytree(
            f"{filename}/{optional_repo_nickname}",
            f"{fusion_path}/{optional_repo_nickname}",
        )
    else:
        shutil.copytree(filename, fusion_path)

    git_mocks = glob.glob(f"{fusion_path}/*/.git_mock")
    for git_mock in git_mocks:
        os.rename(git_mock, git_mock.replace("/.git_mock", "/.git"))


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("organization")
@pytest.mark.parametrize(
    ("email", "role", "permissions"),
    (("admin@gmail.com", "admin", 12),),
)
async def test_get_organization_ver_1(
    populate: bool,
    email: str,
    role: str,
    permissions: int,
) -> None:
    assert populate
    org_id: str = "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db"
    org_name: str = "orgtest"
    org_stakeholders: list[str] = [
        "admin@fluidattacks.com",
        "admin@gmail.com",
        "architect@fluidattacks.com",
        "architect@gmail.com",
        "customer_manager@fluidattacks.com",
        "hacker@fluidattacks.com",
        "hacker@gmail.com",
        "reattacker@fluidattacks.com",
        "reattacker@gmail.com",
        "resourcer@fluidattacks.com",
        "resourcer@gmail.com",
        "reviewer@fluidattacks.com",
        "reviewer@gmail.com",
        "service_forces@fluidattacks.com",
        "service_forces@gmail.com",
        "user@fluidattacks.com",
        "user@gmail.com",
        "user_manager@fluidattacks.com",
        "user_manager@gmail.com",
        "vulnerability_manager@fluidattacks.com",
        "vulnerability_manager@gmail.com",
    ]
    result: dict[str, Any] = await get_result(user=email, org=org_id)
    groups: list[str] = [
        group["name"] for group in result["data"]["organization"]["groups"]
    ]
    stakeholders: list[str] = [
        stakeholder["email"]
        for stakeholder in result["data"]["organization"]["stakeholders"]
    ]
    assert "errors" not in result
    assert result["data"]["organization"]["id"] == org_id
    assert result["data"]["organization"]["inactivityPeriod"] == 180
    assert result["data"]["organization"]["maxAcceptanceDays"] == 90
    assert result["data"]["organization"]["maxAcceptanceSeverity"] == 7
    assert result["data"]["organization"]["maxNumberAcceptances"] == 4
    assert result["data"]["organization"]["minAcceptanceSeverity"] == 3
    assert result["data"]["organization"]["minBreakingSeverity"] == 2
    assert result["data"]["organization"]["vulnerabilityGracePeriod"] == 5
    assert result["data"]["organization"]["name"] == org_name.lower()
    assert sorted(groups) == sorted(["group1", "group3", "unittesting"])
    assert sorted(stakeholders) == sorted(org_stakeholders)
    assert (
        result["data"]["organization"]["integrationRepositoriesConnection"][
            "edges"
        ][0]["node"]["defaultBranch"]
        == "main"
    )
    assert (
        result["data"]["organization"]["integrationRepositoriesConnection"][
            "edges"
        ][0]["node"]["lastCommitDate"]
        == "2022-11-02 04:37:57"
    )
    assert (
        result["data"]["organization"]["integrationRepositoriesConnection"][
            "edges"
        ][0]["node"]["url"]
        == "ssh://git@test.com:v3/testprojects/_git/secondrepor"
    )
    assert len(result["data"]["organization"]["permissions"]) == permissions
    assert result["data"]["organization"]["userRole"] == role
    assert result["data"]["organization"]["coveredAuthors"] == 0
    assert result["data"]["organization"]["coveredCommits"] == 0
    assert result["data"]["organization"]["coveredRepositories"] == 0
    assert result["data"]["organization"]["missedAuthors"] == 0
    assert result["data"]["organization"]["missedCommits"] == 0
    assert result["data"]["organization"]["missedRepositories"] == 0
    assert len(result["data"]["organization"]["credentials"]) == 4
    assert result["data"]["organization"]["credentials"][1]["isPat"] is False
    assert (
        result["data"]["organization"]["credentials"][1]["name"] == "SSH Key"
    )
    assert result["data"]["organization"]["credentials"][3]["isPat"] is True
    assert (
        result["data"]["organization"]["credentials"][3]["name"] == "pat token"
    )

    loaders: Dataloaders = get_new_context()
    current_repositories: tuple[
        OrganizationIntegrationRepository, ...
    ] = await loaders.organization_unreliable_integration_repositories.load(
        (org_id, None, None)
    )
    assert len(current_repositories) == 1
    assert (
        next(
            (
                repository
                for repository in current_repositories
                if repository.branch == "trunk"
            ),
            None,
        )
        is None
    )

    with (
        mock.patch(
            "db_model.azure_repositories.get._get_repositories",
            side_effect=get_repositories,
        ),
        mock.patch(
            "db_model.azure_repositories.get._get_repositories_commits",
            side_effect=get_repositories_commits,
        ),
        mock.patch(
            "db_model.azure_repositories.get._get_repositories_stats",
            side_effect=get_repositories_stats,
        ),
        mock.patch(
            "db_model.azure_repositories.get._get_gitlab_projects",
            side_effect=get_lab_repositories_stats,
        ),
        mock.patch(
            "db_model.azure_repositories.get._get_gitlab_commit",
            side_effect=get_lab_commit_stats,
        ),
        mock.patch(
            "db_model.azure_repositories.get._get_github_repos",
            side_effect=get_hub_repositories_stats,
        ),
        mock.patch(
            "db_model.azure_repositories.get._get_github_repos_commits",
            side_effect=get_hub_commit_stats,
        ),
    ):
        await update_organization_repositories()

    with (
        mock.patch(
            "azure_repositories.domain.pull_repositories",
            side_effect=mocked_pull_repositories,
        ),
        mock.patch(
            "azure_repositories.domain.get_covered_group",
            side_effect=get_covered_group,
        ),
        mock.patch(
            "azure_repositories.domain._get_missed_authors",
            side_effect=_get_missed_authors,
        ),
        mock.patch(
            "db_model.azure_repositories.get._get_repositories",
            side_effect=get_repositories,
        ),
        mock.patch(
            "db_model.azure_repositories.get._get_repositories_commits",
            side_effect=get_repositories_commits,
        ),
        mock.patch(
            "db_model.azure_repositories.get._get_gitlab_projects",
            side_effect=get_lab_repositories_stats,
        ),
        mock.patch(
            "db_model.azure_repositories.get._get_gitlab_commit",
            side_effect=get_lab_commit_stats,
        ),
        mock.patch(
            "db_model.azure_repositories.get._get_github_repos",
            side_effect=get_hub_repositories_stats,
        ),
        mock.patch(
            "db_model.azure_repositories.get._get_github_repos_commits",
            side_effect=get_hub_commit_stats,
        ),
    ):
        await update_organization_overview()

    result = await get_result(user=email, org=org_id)
    assert "errors" not in result
    assert result["data"]["organization"]["coveredAuthors"] == 1
    assert result["data"]["organization"]["coveredCommits"] == 12
    assert result["data"]["organization"]["coveredRepositories"] == 1
    assert result["data"]["organization"]["missedAuthors"] == 3
    assert result["data"]["organization"]["missedCommits"] == 12
    assert result["data"]["organization"]["missedRepositories"] == 3

    loaders.organization_unreliable_integration_repositories.clear_all()
    current_repositories = (
        await loaders.organization_unreliable_integration_repositories.load(
            (org_id, None, None)
        )
    )
    assert len(current_repositories) == 3
    assert (
        next(
            (
                repository
                for repository in current_repositories
                if repository.branch == "refs/head/trunk"
            ),
            None,
        )
        is not None
    )

    result_remove = await remove_credentials(
        user="user_manager@fluidattacks.com",
        credentials_id="1a5dacda-1d52-465c-9158-f6fd5dfe0998",
        organization_id=org_id,
    )
    assert "errors" not in result_remove
    assert "success" in result_remove["data"]["removeCredentials"]
    assert result_remove["data"]["removeCredentials"]["success"]

    result_remove = await remove_credentials(
        user="user_manager@fluidattacks.com",
        credentials_id="c9ecb25c-8d9f-422c-abc4-44c0c700a760",
        organization_id=org_id,
    )
    assert "errors" not in result_remove
    assert "success" in result_remove["data"]["removeCredentials"]
    assert result_remove["data"]["removeCredentials"]["success"]

    result_remove = await remove_credentials(
        user="user_manager@fluidattacks.com",
        credentials_id="5b81d698-a5bc-4dda-bdf9-40d0725358b4",
        organization_id=org_id,
    )
    assert "errors" not in result_remove
    assert "success" in result_remove["data"]["removeCredentials"]
    assert result_remove["data"]["removeCredentials"]["success"]

    loaders.organization_unreliable_integration_repositories.clear_all()
    current_repositories = (
        await loaders.organization_unreliable_integration_repositories.load(
            (org_id, None, None)
        )
    )
    assert len(current_repositories) == 3

    await update_organization_repositories()
    with mock.patch(
        "azure_repositories.domain.pull_repositories",
        side_effect=mocked_pull_repositories,
    ):
        await update_organization_overview()

    loaders.organization_unreliable_integration_repositories.clear_all()
    loaders.organization_credentials.clear_all()
    loaders.group_roots.clear_all()

    updated_repositories: tuple[
        OrganizationIntegrationRepository, ...
    ] = await loaders.organization_unreliable_integration_repositories.load(
        (org_id, None, None)
    )
    assert len(updated_repositories) == 0

    result = await get_result(user=email, org=org_id)
    assert "errors" not in result
    assert result["data"]["organization"]["coveredAuthors"] == 0
    assert result["data"]["organization"]["coveredCommits"] == 0
    assert result["data"]["organization"]["coveredRepositories"] == 1
    assert result["data"]["organization"]["missedAuthors"] == 0
    assert result["data"]["organization"]["missedCommits"] == 0
    assert result["data"]["organization"]["missedRepositories"] == 0


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("organization")
@pytest.mark.parametrize(
    ("email", "role", "permissions"),
    (
        ("user@gmail.com", "user", 3),
        ("user_manager@gmail.com", "user_manager", 29),
        ("vulnerability_manager@gmail.com", "user", 3),
        ("hacker@gmail.com", "user", 3),
        ("reattacker@gmail.com", "user", 3),
        ("resourcer@gmail.com", "user", 3),
        ("reviewer@gmail.com", "user", 3),
        ("customer_manager@fluidattacks.com", "customer_manager", 27),
    ),
)
async def test_get_organization_ver_2(
    populate: bool, email: str, role: str, permissions: int
) -> None:
    assert populate
    org_id: str = "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db"
    org_name: str = "orgtest"
    org_groups: list[str] = [
        "group1",
    ]
    result: dict[str, Any] = await get_result(user=email, org=org_id)
    groups: list[str] = [
        group["name"] for group in result["data"]["organization"]["groups"]
    ]
    assert result["data"]["organization"]["id"] == org_id
    assert result["data"]["organization"]["inactivityPeriod"] == 180
    assert result["data"]["organization"]["maxAcceptanceDays"] == 90
    assert result["data"]["organization"]["maxAcceptanceSeverity"] == 7
    assert result["data"]["organization"]["maxNumberAcceptances"] == 4
    assert result["data"]["organization"]["minAcceptanceSeverity"] == 3
    assert result["data"]["organization"]["minBreakingSeverity"] == 2
    assert result["data"]["organization"]["vulnerabilityGracePeriod"] == 5
    assert result["data"]["organization"]["name"] == org_name.lower()
    assert org_groups[0] in groups
    assert len(result["data"]["organization"]["permissions"]) == permissions
    assert result["data"]["organization"]["userRole"] == role


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("organization")
@pytest.mark.parametrize(
    ("email", "role", "permissions"),
    (("admin@gmail.com", "admin", 12),),
)
async def test_get_organization_default_values(
    populate: bool, email: str, role: str, permissions: int
) -> None:
    assert populate
    org_id: str = "ORG#8a7c8089-92df-49ec-8c8b-ee83e4ff3256"
    org_name: str = "acme"
    org_stakeholders: list[str] = [
        "admin@gmail.com",
    ]
    result: dict[str, Any] = await get_result(user=email, org=org_id)
    groups: list[str] = [
        group["name"] for group in result["data"]["organization"]["groups"]
    ]
    stakeholders: list[str] = [
        stakeholder["email"]
        for stakeholder in result["data"]["organization"]["stakeholders"]
    ]
    assert "errors" not in result
    assert result["data"]["organization"]["id"] == org_id
    assert result["data"]["organization"]["inactivityPeriod"] == 90
    assert result["data"]["organization"]["maxAcceptanceDays"] is None
    assert result["data"]["organization"]["maxAcceptanceSeverity"] == 10.0
    assert result["data"]["organization"]["maxNumberAcceptances"] is None
    assert result["data"]["organization"]["minAcceptanceSeverity"] == 0.0
    assert result["data"]["organization"]["minBreakingSeverity"] == 0.0
    assert result["data"]["organization"]["vulnerabilityGracePeriod"] == 0
    assert result["data"]["organization"]["name"] == org_name.lower()
    assert sorted(groups) == []
    assert sorted(stakeholders) == org_stakeholders
    assert len(result["data"]["organization"]["permissions"]) == permissions
    assert result["data"]["organization"]["userRole"] == role
    assert len(result["data"]["organization"]["credentials"]) == 0


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("organization")
@pytest.mark.parametrize(
    ("email", "verification_code"),
    (
        ("admin@gmail.com", None),
        ("admin@gmail.com", "123123"),
    ),
)
async def test_get_org_vulnerabilities_url(
    populate: bool, email: str, verification_code: Optional[str]
) -> None:
    assert populate
    org_id: str = "ORG#8a7c8089-92df-49ec-8c8b-ee83e4ff3256"
    result: dict[str, Any] = await get_vulnerabilities_url(
        user=email,
        org_id=org_id,
        verification_code=verification_code,
        session_jwt=None,
    )
    if verification_code:
        assert "errors" not in result
        assert (
            result["data"]["organization"]["vulnerabilitiesUrl"]
            == "https://test.com"
        )
    else:
        assert "errors" in result
        assert result["errors"][0]["message"] == str(
            RequiredVerificationCode()
        )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("organization")
@pytest.mark.parametrize(
    ("email", "verification_code"),
    (("admin@gmail.com", None),),
)
async def test_get_org_vulnerabilities_url_api(
    populate: bool, email: str, verification_code: Optional[str]
) -> None:
    assert populate
    org_id: str = "ORG#8a7c8089-92df-49ec-8c8b-ee83e4ff3256"
    result_1: dict[str, Any] = await get_vulnerabilities_url(
        user=email,
        org_id=org_id,
        verification_code=verification_code,
        session_jwt=None,
    )
    assert "errors" in result_1
    assert result_1["errors"][0]["message"] == str(RequiredVerificationCode())

    ts_expiration_time: int = int(
        (datetime.utcnow() + timedelta(weeks=8)).timestamp()
    )
    result_jwt = await get_access_token(
        user=email,
        expiration_time=ts_expiration_time,
    )
    assert "errors" not in result_jwt
    assert result_jwt["data"]["updateAccessToken"]["success"]

    session_jwt: str = result_jwt["data"]["updateAccessToken"]["sessionJwt"]
    result_2: dict[str, Any] = await get_vulnerabilities_url(
        user=email,
        org_id=org_id,
        verification_code=verification_code,
        session_jwt=session_jwt,
    )

    assert "errors" not in result_2
    assert (
        result_2["data"]["organization"]["vulnerabilitiesUrl"]
        == "https://test.com"
    )
