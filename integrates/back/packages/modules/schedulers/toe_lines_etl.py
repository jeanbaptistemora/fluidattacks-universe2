# Standard libraries
import csv
from typing import (
    Any,
    Callable,
    List,
    Tuple,
)

# Local libraries
from dynamodb.types import (
    GitRootToeLines,
)
from newutils import (
    datetime as datetime_utils,
)
from roots import domain as roots_domain
from roots.types import Root


def _format_date(date_str: str) -> str:
    date = datetime_utils.get_from_str(date_str, date_format='%Y-%m-%d')
    formated_date_str = datetime_utils.get_as_str(date)

    return formated_date_str


def _get_group_toe_lines_from_cvs(
    lines_csv_path: str,
    group_name: str,
    group_roots: Tuple[Root, ...]
) -> Tuple[GitRootToeLines, ...]:
    default_date = datetime_utils.DEFAULT_STR
    lines_csv_fields: List[Tuple[str, Callable, Any, str]] = [
        # field_name, field_formater, field_default_value, cvs_field_name,
        ('filename', str, '', 'filename'),
        ('comments', str, '', 'comments'),
        ('modified_commit', str, '', 'modified-commit'),
        ('loc', int, 0, 'loc'),
        ('tested_lines', int, 0, 'tested-lines'),
        ('modified_date', _format_date, default_date, 'modified-date'),
        ('tested_date', _format_date, default_date, 'tested-date'),
    ]
    group_toe_lines = list()
    with open(lines_csv_path) as csv_file:
        for row in csv.DictReader(csv_file):
            new_toe_lines = dict()
            for (
                field_name,
                formater,
                default_value,
                cvs_field_name
            ) in lines_csv_fields:
                cvs_field_value = row.get(cvs_field_name)
                try:
                    new_toe_lines[field_name] = (
                        formater(cvs_field_value)
                        if cvs_field_value
                        else default_value
                    )
                except ValueError:
                    new_toe_lines[field_name] = default_value

            new_toe_lines['root_id'] = roots_domain.get_root_id_by_filename(
                row['filename'],
                group_roots
            )
            new_toe_lines['group_name'] = group_name
            group_toe_lines.append(GitRootToeLines(**new_toe_lines))

    return tuple(group_toe_lines)


def _get_toe_lines_to_update(
    group_toe_lines: Tuple[GitRootToeLines, ...],
    cvs_group_toe_lines: Tuple[GitRootToeLines, ...]
) -> Tuple[GitRootToeLines, ...]:
    return tuple([
        toe_lines
        for toe_lines in cvs_group_toe_lines
        if toe_lines not in group_toe_lines
    ])
