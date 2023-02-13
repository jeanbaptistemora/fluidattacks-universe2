from collections.abc import (
    Callable,
)
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
from utils.logs import (
    log,
)


def run_tests_gitlab(
    config: Dynaconf,
    pull_request: PullRequest,
) -> bool:
    success: bool = True

    log("info", "Reviewing PR: %s", pull_request.url)
    if not tests.skip_ci(pull_request):
        syntax: Syntax = Syntax(
            user_regex=config["syntax"]["user_regex"],
        )
        for name, args in config["tests"].items():
            data: TestData = TestData(
                config=args,
                pull_request=pull_request,
                syntax=syntax,
            )
            test: Callable[[], bool] = partial(getattr(tests, name), data=data)
            log("info", "Running tests.%s", name)
            success = test() and success
            if (
                not success
                and args["close_pr"]
                and pull_request.state() not in ("closed", "merged")
            ):
                gl.close_pr(pull_request=pull_request)
                log("error", "Merge Request closed by: %s", name)

    return success


def run(config_path: str) -> bool:
    success: bool = False
    verify_required_vars(["REVIEWS_TOKEN"])
    config: Dynaconf = load(config_path)

    if config["platform"] in "gitlab":
        verify_required_vars(["CI_MERGE_REQUEST_IID"])
        project: GitlabProject = gl.get_project(  # type: ignore
            url=config["endpoint_url"],
            token=str(os.environ.get("REVIEWS_TOKEN")),
            project_id=config["project_id"],
        )
        pull_request_id: str = str(os.environ.get("CI_MERGE_REQUEST_IID"))
        pull_request: PullRequest = gl.get_pull_request(
            project=project, pull_request_id=pull_request_id  # type: ignore
        )

        success = run_tests_gitlab(
            config,
            pull_request,
        )
    else:
        log(
            "error",
            "platform is %s. Only 'gitlab' supported for now.",
            config["platform"],
        )

    return success
