from config import (
    load,
)
from core import (
    tests,
)
from dal import (
    gl,
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
from gitlab.v4.objects import (
    Project as GitlabProject,
)
import os
from typing import (
    Callable,
)
from utils.logs import (
    log,
)


def run_tests_gitlab(
    config: Dynaconf,
    pull_request: PullRequest,
) -> bool:
    success = True

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
                gl.close_pr(pull_request)
                log("error", "Merge Request closed by: %s", name)

    return success


def run(legacy: bool, config_path: str) -> bool:
    success: bool = True
    verify_required_vars(["REVIEWS_TOKEN"])
    config: Dynaconf = load(config_path)

    if config["platform"] in "gitlab":
        project: GitlabProject = gl.get_project(
            config["endpoint_url"],
            str(os.environ.get("REVIEWS_TOKEN")),
            config["project_id"],
        )

        if legacy:
            verify_required_vars(["CI_MERGE_REQUEST_IID"])
            pull_request_id: str = str(os.environ.get("CI_MERGE_REQUEST_IID"))
            pull_request: PullRequest = gl.get_pull_request(
                project, pull_request_id
            )

            success = run_tests_gitlab(
                config,
                pull_request,
            )
        else:
            for pull_request in gl.get_pull_requests(project).values():
                run_tests_gitlab(config, pull_request)

    return success
