from config import (
    load,
)
from core import (
    tests,
)
from dal import (
    gitlab,
    verify_required_vars,
)
from dal.model import (
    PullRequest,
    Syntax,
    TestData,
)
from dynaconf import (
    Dynaconf,
)
from functools import (
    partial,
)
from gitlab import (
    Gitlab,
)
import os
from typing import (
    Callable,
)
from utils.logs import (
    log,
)


def run_tests_gitlab(
    session: Gitlab,
    config: Dynaconf,
    project_id: str,
    mr_iid: str,
) -> bool:
    success = True
    pull_request: PullRequest = gitlab.get_pr(session, project_id, mr_iid)

    if not tests.skip_ci(pull_request):
        syntax: Syntax = Syntax(
            match_groups=config["syntax"]["match_groups"],
            regex=config["syntax"]["regex"],
            user_regex=config["syntax"]["user_regex"],
        )
        for name, args in config["tests"].items():
            data: TestData = TestData(
                config=args,
                pull_request=pull_request,
                syntax=syntax,
            )
            test: Callable[[], bool] = partial(getattr(tests, name), data=data)
            log("info", f"Running tests.{name}")
            success = test() and success
            if (
                not success
                and args["close_pr"]
                and pull_request.raw.state not in "closed"
            ):
                gitlab.close_pr(pull_request)
                log("error", "Merge Request closed by: %s", name)

    return success


def run(legacy: bool, config_path: str) -> bool:
    success: bool = True
    verify_required_vars(["REVIEWS_TOKEN"])
    config: Dynaconf = load(config_path)

    if config["platform"] in "gitlab":
        session: Gitlab = gitlab.login(
            config["endpoint_url"],
            str(os.environ.get("REVIEWS_TOKEN")),
        )
        verify_required_vars(["CI_PROJECT_ID"])
        project_id: str = str(os.environ.get("CI_PROJECT_ID"))

        if legacy:
            verify_required_vars(["CI_MERGE_REQUEST_IID"])
            mr_iid: str = str(os.environ.get("CI_MERGE_REQUEST_IID"))
            success = (
                run_tests_gitlab(
                    session,
                    config,
                    project_id,
                    mr_iid,
                )
                and success
            )
        else:
            pull_requests: list[PullRequest] = gitlab.get_prs(
                session, project_id, "opened"
            )
            for pull_request in pull_requests:
                run_tests_gitlab(session, config, project_id, pull_request.iid)

    return success
