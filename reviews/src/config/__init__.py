# Standard libraries
from typing import Any, Dict, List

# Third party libraries
from dynaconf import Dynaconf, Validator


ERR_DEFAULT: Dict[str, str] = {
    "must_exist_true": "{name} is required.",
    "must_exist_false": "{name} cannot exist.",
    "condition": "{name} invalid for {function}({value}).",
    "operations": "{name} must be {op_value}.",
    "combined": "combined validators failed {errors}.",
}


def dict_has_type_values(
    dictionary: Dict[str, Any], expected_type: type
) -> bool:
    success: bool = True
    for value in dictionary.values():
        if not isinstance(value, expected_type):
            success = False
            break
    return success


def validate_base(config: Dynaconf) -> None:
    config.validators.register(
        Validator(
            "endpoint_url",
            "platform",
            "syntax.regex",
            "tests",
            must_exist=True,
            messages=ERR_DEFAULT,
        ),
        Validator(
            "syntax.match_groups",
            must_exist=True,
            condition=lambda x: dict_has_type_values(x, int),
            messages={
                "must_exist_true": "{name} is required.",
                "condition": "{name} invalid. " "All values must be int",
            },
        ),
    )
    config.validators.validate()
    tests: List[str] = list(config["tests"].keys())
    for test in tests:
        config.validators.register(
            Validator(
                f"tests.{test}.fail",
                f"tests.{test}.close_pr",
                must_exist=True,
                is_type_of=bool,
                messages=ERR_DEFAULT,
            ),
        )


def validate_specific(config: Dynaconf) -> None:
    tests: List[str] = list(config["tests"].keys())
    for test in tests:
        if test in ("commits_user_syntax", "pr_user_syntax"):
            config.validators.register(
                Validator(
                    "syntax.user_regex",
                    must_exist=True,
                    is_type_of=str,
                    messages=ERR_DEFAULT,
                ),
            )
        elif test in "all_pipelines_successful":
            config.validators.register(
                Validator(
                    f"tests.{test}.job_name",
                    must_exist=True,
                    is_type_of=str,
                    messages=ERR_DEFAULT,
                ),
            )
        elif test in "pr_under_max_deltas":
            config.validators.register(
                Validator(
                    f"tests.{test}.max_deltas",
                    must_exist=True,
                    is_type_of=int,
                    messages=ERR_DEFAULT,
                ),
                Validator(
                    f"tests.{test}.repo_path",
                    must_exist=True,
                    is_type_of=str,
                    messages=ERR_DEFAULT,
                ),
            )
        elif test in "most_relevant_type":
            config.validators.register(
                Validator(
                    f"tests.{test}.relevances",
                    must_exist=True,
                    condition=lambda x: dict_has_type_values(x, int),
                    messages={
                        "must_exist_true": "{name} is required.",
                        "condition": "{name} invalid. "
                        "All values must be int",
                    },
                ),
                Validator(
                    "syntax.match_groups.type",
                    must_exist=True,
                    is_type_of=int,
                    messages=ERR_DEFAULT,
                ),
            )
        elif test in "pr_max_commits":
            config.validators.register(
                Validator(
                    f"tests.{test}.max_commits",
                    must_exist=True,
                    is_type_of=int,
                    messages=ERR_DEFAULT,
                ),
            )
        elif test in "close_issue_directive":
            config.validators.register(
                Validator(
                    "syntax.match_groups.issue",
                    must_exist=True,
                    is_type_of=int,
                    messages=ERR_DEFAULT,
                ),
            )
        elif test in "pr_only_one_product":
            config.validators.register(
                Validator(
                    "syntax.match_groups.product",
                    must_exist=True,
                    is_type_of=int,
                    messages=ERR_DEFAULT,
                ),
            )
    config.validators.validate()


def validate(conf: Dynaconf) -> None:
    validate_base(conf)
    validate_specific(conf)


def load(config_path: str) -> Dynaconf:
    config: Dynaconf = Dynaconf(
        envvar_prefix="REVIEWS",
        settings_files=[config_path],
    )
    validate(config)
    return config
