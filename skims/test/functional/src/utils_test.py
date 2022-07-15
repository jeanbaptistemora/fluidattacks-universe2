from cli import (
    cli,
)
from contextlib import (
    redirect_stderr,
    redirect_stdout,
)
import csv
import io
from itertools import (
    zip_longest,
)
import os
from typing import (
    Callable,
    Dict,
    Iterable,
    List,
    Text,
    Tuple,
)
from utils.logs import (
    configure,
)


def skims(*args: str) -> Tuple[int, str, str]:
    out_buffer, err_buffer = io.StringIO(), io.StringIO()

    with redirect_stdout(out_buffer), redirect_stderr(err_buffer):
        try:
            configure()
            cli.main(args=list(args), prog_name="skims")
        except SystemExit as exc:  # NOSONAR
            code: int = exc.code

    try:
        return code, out_buffer.getvalue(), err_buffer.getvalue()
    finally:
        del out_buffer
        del err_buffer


def get_suite_config(suite: str) -> str:
    return f"skims/test/data/config/{suite}.yaml"


def _default_snippet_filter(snippet: str) -> str:
    return snippet


def get_suite_produced_results(suite: str) -> str:
    return f"skims/test/outputs/{suite}.csv"


def get_suite_expected_results(suite: str) -> str:
    return f"skims/test/data/results/{suite}.csv"


def _format_csv(
    content: Iterable[Text],
    *,
    snippet_filter: Callable[[str], str],
) -> List[Dict[str, str]]:
    result: List[Dict[str, str]] = []
    for row in csv.DictReader(content):
        row["snippet"] = snippet_filter(row["snippet"])
        result.append(row)
    result.sort(key=str)
    return result


def check_that_csv_results_match(
    suite: str,
    *,
    snippet_filter: Callable[[str], str] = _default_snippet_filter,
) -> None:
    with open(get_suite_produced_results(suite), encoding="utf-8") as produced:
        expected_path = os.path.join(
            os.environ["STATE"], get_suite_expected_results(suite)
        )
        os.makedirs(os.path.dirname(expected_path), exist_ok=True)
        with open(expected_path, "w", encoding="utf-8") as expected:
            expected.write(produced.read())
            produced.seek(0)

        with open(
            get_suite_expected_results(suite), encoding="utf-8"
        ) as expected:
            for producted_item, expected_item in zip_longest(
                _format_csv(produced, snippet_filter=snippet_filter),
                _format_csv(expected, snippet_filter=snippet_filter),
                fillvalue=None,
            ):
                assert producted_item == expected_item
