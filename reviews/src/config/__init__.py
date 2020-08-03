# Standard libraries
from typing import Any, Dict, List

# Third party libraries
from dynaconf import Dynaconf, Validator

def get_validators() -> List[Any]:

    def dict_has_type_values(dictionary: Dict[str, Any], expected_type: type) -> bool:
        success: bool = True
        for value in dictionary.values():
            if not isinstance(value, expected_type):
                success = False
        return success

    validators: List[Any] = [
        # base
        Validator('gitlab_url', 'tests', must_exist=True),

        # all_pipelines_successful
        Validator('tests.all_pipelines_successful', must_exist=False)
        | Validator('tests.all_pipelines_successful.fail',
                    must_exist=True, is_type_of=bool),

        # mr_message_syntax
        Validator('tests.mr_message_syntax', must_exist=False)
        | Validator('tests.mr_message_syntax.fail',
                    must_exist=True, is_type_of=bool),

        # branch_equals_to_user
        Validator('tests.branch_equals_to_user', must_exist=False)
        | Validator('tests.branch_equals_to_user.fail',
                    must_exist=True, is_type_of=bool),

        # mr_under_max_deltas
        Validator('tests.mr_under_max_deltas', must_exist=False)
        | Validator('tests.mr_under_max_deltas.fail',
                     must_exist=True, is_type_of=bool)
        & Validator('tests.mr_under_max_deltas.max_deltas',
                    must_exist=True, is_type_of=int)
        & Validator('tests.mr_under_max_deltas.repo_path',
                    must_exist=True, is_type_of=str),

        # most_relevant_type
        Validator('tests.most_relevant_type', must_exist=False)
        | Validator('tests.most_relevant_type.fail',
                    must_exist=True, is_type_of=bool)
        & Validator('tests.most_relevant_type.commit_regex',
                    must_exist=True, is_type_of=str)
        & Validator('tests.most_relevant_type.relevances', must_exist=True,
                    condition=lambda x: dict_has_type_values(x, int)),

        # commits_user_syntax
        Validator('tests.commits_user_syntax', must_exist=False)
        | Validator('tests.commits_user_syntax.fail',
                    must_exist=True, is_type_of=bool)
        & Validator('tests.commits_user_syntax.user_regex',
                    must_exist=True, is_type_of=str),

        # mr_user_syntax
        Validator('tests.mr_user_syntax', must_exist=False)
        | Validator('tests.mr_user_syntax.fail',
                    must_exist=True, is_type_of=bool)
        & Validator('tests.mr_user_syntax.user_regex',
                    must_exist=True, is_type_of=str),

        # max_commits_per_mr
        Validator('tests.max_commits_per_mr',
                    must_exist=False)
        | Validator('tests.max_commits_per_mr.fail',
                    must_exist=True, is_type_of=bool)
        & Validator('tests.max_commits_per_mr.max_commits',
                    must_exist=True, is_type_of=int),

        # close_issue_directive
        Validator('tests.close_issue_directive', must_exist=False)
        | Validator('tests.close_issue_directive.fail',
                    must_exist=True, is_type_of=bool)
        & Validator('tests.close_issue_directive.mr_title_regex',
                    must_exist=True, is_type_of=str),
    ]

    return validators


def load(config_path: str) -> Any:
    config = Dynaconf(
        envvar_prefix='REVIEWS',
        settings_files=[config_path],
        validators=get_validators(),
    )
    config.validators.validate()
    return config
