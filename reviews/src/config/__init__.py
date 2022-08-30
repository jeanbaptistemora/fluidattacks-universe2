from dynaconf import (
    Dynaconf,
    Validator,
)
from typing import (
    Any,
)

ERR_DEFAULT: dict[str, str] = {
    "must_exist_true": "{name} is required.",
    "must_exist_false": "{name} cannot exist.",
    "condition": "{name} invalid for {function}({value}).",
    "operations": "{name} must be {op_value}.",
    "combined": "combined validators failed {errors}.",
}


def dict_has_type_values(
    dictionary: dict[str, Any], expected_type: type
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
            "platform",
            "endpoint_url",
            "project_id",
            "tests",
            must_exist=True,
            messages=ERR_DEFAULT,
        ),
    )
    config.validators.validate()
    tests: list[str] = list(config["tests"].keys())
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
    tests: list[str] = list(config["tests"].keys())
    for test in tests:
        if test in ("commit_user_syntax", "pr_user_syntax"):
            config.validators.register(
                Validator(
                    "syntax.user_regex",
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
        elif test in "pr_max_commits":
            config.validators.register(
                Validator(
                    f"tests.{test}.max_commits",
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
