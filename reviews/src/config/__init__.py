# Standard libraries
from typing import Any, Dict, List

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

    err_default: Dict[str,str] = {
        'must_exist_true': '{name} is required.',
        'must_exist_false': '{name} cannot exist.',
        'condition': '{name} invalid for {function}({value}).',
        'operations': '{name} must be {op_value}.',
        'combined': 'combined validators failed {errors}.',
    }

    # Validate main keys
    config.validators.register(
        Validator('gitlab_url', 'tests', must_exist=True,
                  messages=err_default),
    )
    config.validators.validate()

    # Validate tests
    tests: List[str] = list(config['tests'].keys())
    for test in tests:
        config.validators.register(
            Validator(f'tests.{test}.fail', f'tests.{test}.close_mr',
                      must_exist=True, is_type_of=bool, messages=err_default),
        )
        if test in ('commits_user_syntax', 'mr_user_syntax'):
            config.validators.register(
                Validator(f'tests.{test}.user_regex', must_exist=True,
                          is_type_of=str, messages=err_default),
            )
        if test in 'all_pipelines_successful':
            config.validators.register(
                Validator(f'tests.{test}.passed_first_pipeline_before_mr',
                          must_exist=True, is_type_of=bool,
                          messages=err_default),
            )
        if test in 'mr_under_max_deltas':
            config.validators.register(
                Validator(f'tests.{test}.max_deltas', must_exist=True,
                          is_type_of=int, messages=err_default),
                Validator(f'tests.{test}.repo_path', must_exist=True,
                          is_type_of=str, messages=err_default),
            )
        if test in 'most_relevant_type':
            config.validators.register(
                Validator(f'tests.{test}.commit_regex', must_exist=True,
                          is_type_of=str, messages=err_default),
                Validator(f'tests.{test}.relevances', must_exist=True,
                          condition=lambda x: dict_has_type_values(x, int),
                          messages={'must_exist_true': '{name} is required.',
                                    'condition': '{name} invalid. '
                                    'All values must be int'}),
            )
        if test in 'max_commits_per_mr':
            config.validators.register(
                Validator(f'tests.{test}.max_commits', must_exist=True,
                          is_type_of=int, messages=err_default),
            )
        if test in 'close_issue_directive':
            config.validators.register(
                Validator(f'tests.{test}.mr_title_regex', must_exist=True,
                          is_type_of=str, messages=err_default),
            )
    config.validators.validate()


def load(config_path: str) -> Dynaconf:
    config: Dynaconf = Dynaconf(
        envvar_prefix='REVIEWS',
        settings_files=[config_path],
    )
    validate(config)
    return config
