# Standard library
import os
import csv
import sys
from typing import (
    Dict,
    NamedTuple,
)

# Local libraries
from utils.logs import (
    blocking_log,
)


class Score(NamedTuple):
    false_negatives: int
    false_positives: int
    false_positives_rate: float
    score: float
    true_negatives: int
    true_positives: int
    true_positives_rate: float


def cast_to_boolean(boolean: str) -> bool:
    if boolean == 'false':
        return False

    if boolean == 'true':
        return True

    raise NotImplementedError(boolean)


def load_benchmark_results() -> Dict[str, bool]:
    """Return a mapping from test to boolean indicating vulnerability state.

    Example:

        >>> { "BenchmarkTest02735": True }  # The test 02735 is vulnerable
    """
    with open(os.environ['EXPECTED_RESULTS_CSV']) as file:
        mapping: Dict[str, bool] = {
            row['# test name']: cast_to_boolean(row[' real vulnerability'])
            for row in csv.DictReader(file)
        }

    return mapping


def load_skims_results() -> Score:
    false_negatives: int = 0
    false_positives: int = 0
    true_negatives: int = 0
    true_positives: int = 0

    skims_stdout: str = sys.stdin.read()

    for test, is_vulnerable in load_benchmark_results().items():
        is_safe: bool = not is_vulnerable
        skims_said_is_vulnerable: bool = test in skims_stdout
        skims_said_is_safe: bool = not skims_said_is_vulnerable

        if skims_said_is_safe and is_safe:
            true_negatives += 1
        elif skims_said_is_safe and not is_safe:
            false_negatives += 1
        elif skims_said_is_vulnerable and is_vulnerable:
            true_positives += 1
        elif skims_said_is_vulnerable and not is_vulnerable:
            false_positives += 1
        else:
            raise NotImplementedError()

    true_positives_rate: float = true_positives / (
        true_positives + false_negatives
    )
    false_positives_rate: float = false_positives / (
        false_positives + true_negatives
    )
    score: float = true_positives_rate - false_positives_rate

    return Score(
        false_negatives=false_negatives,
        false_positives=false_positives,
        true_negatives=true_negatives,
        true_positives=true_positives,
        true_positives_rate=true_positives_rate,
        false_positives_rate=false_positives_rate,
        score=score,
    )


def main() -> None:
    score: Score = load_skims_results()

    for attr, attr_value in (
        ('skims_false_negatives', score.false_negatives),
        ('skims_false_positives', score.false_positives),
        ('skims_true_negatives', score.true_negatives),
        ('skims_true_positives', score.true_positives),
        ('skims_true_positives_rate', score.true_positives_rate),
        ('skims_false_positives_rate', score.false_positives_rate),
        ('skims_score', score.score),
    ):
        blocking_log('info', '%s: %s', attr, attr_value)


if __name__ == '__main__':
    main()
