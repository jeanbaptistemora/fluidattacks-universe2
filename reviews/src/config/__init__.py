# Standard libraries
from typing import Any, Dict, List
from types import MappingProxyType

# Third party libraries
from dynaconf import Dynaconf, Validator


def validate(config: Dynaconf) -> None:

    def dict_has_type_values(dictionary: Dict[str, Any], expected_type: type) -> bool:
        success: bool = True
        for value in dictionary.values():
            if not isinstance(value, expected_type):
                success = False
                break
        return success

    # Validate main keys
    config.validators.register(
        Validator('gitlab_url', 'tests', must_exist=True)
    )
    config.validators.validate()

    # Validate tests
    tests: List[str] = list(config['tests'].keys())
    for test in tests:
        config.validators.register(
            Validator(f'tests.{test}.fail',
                      must_exist=True, is_type_of=bool),
        )
        if test in ('commits_user_syntax', 'mr_user_syntax'):
            config.validators.register(
                Validator(f'tests.{test}.user_regex',
                          must_exist=True, is_type_of=str),
            )
        if test in 'mr_under_max_deltas':
            config.validators.register(
                Validator(f'tests.{test}.max_deltas',
                          must_exist=True, is_type_of=int),
                Validator(f'tests.{test}.repo_path',
                          must_exist=True, is_type_of=str),
            )
        if test in 'most_relevant_type':
            config.validators.register(
                Validator(f'tests.{test}.commit_regex',
                          must_exist=True, is_type_of=str),
                Validator(f'tests.{test}.relevances', must_exist=True,
                          condition=lambda x: dict_has_type_values(x, int)),
            )
        if test in 'max_commits_per_mr':
            config.validators.register(
                Validator(f'tests.{test}.max_commits',
                          must_exist=True, is_type_of=int),
            )
        if test in 'close_issue_directive':
            config.validators.register(
                Validator(f'tests.{test}.mr_title_regex',
                          must_exist=True, is_type_of=str),
            )
    config.validators.validate()


def load(config_path: str) -> Dynaconf:
    config: Dynaconf = Dynaconf(
        envvar_prefix='REVIEWS',
        settings_files=[config_path],
    )
    validate(config)
    return config
