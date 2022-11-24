import csv
import glob
import json
import os
from typing import (
    Any,
    Dict,
    List,
    NamedTuple,
    Optional,
    Tuple,
)
from utils.logs import (
    log_blocking,
)


class Result(NamedTuple):
    cwe: Tuple[str, ...]
    is_vulnerable: bool

    category: Optional[str] = None

    def shares_cwe_with(self, other: "Result") -> bool:
        return bool(set(self.cwe).intersection(set(other.cwe)))


class Score(NamedTuple):
    false_negatives: int
    false_positives: int
    false_positives_rate: float
    score: float
    true_negatives: int
    true_positives: int
    true_positives_rate: float


def cast_to_boolean(boolean: str) -> bool:
    if boolean == "false":
        return False

    if boolean == "true":
        return True

    raise NotImplementedError(boolean)


def load_benchmark_expected_results() -> Dict[str, Result]:
    with open(os.environ["EXPECTED_RESULTS_CSV"], encoding="utf-8") as file:
        mapping: Dict[str, Result] = {
            row["# test name"]
            + ".java": Result(
                category=row[" category"],
                cwe=(row[" cwe"],),
                is_vulnerable=is_vulnerable,
            )
            for row in csv.DictReader(file)
            for is_vulnerable in [cast_to_boolean(row[" real vulnerability"])]
        }

    return mapping


def load_benchmark_skims_results() -> Dict[str, List[Result]]:
    mapping: Dict[str, List[Result]] = {}

    for path in glob.glob("skims/test/outputs/benchmark_owasp_*.csv"):
        with open(path, encoding="utf-8") as file:
            for row in csv.DictReader(file):
                what = os.path.basename(row["what"])
                mapping.setdefault(what, [])
                mapping[what].append(
                    Result(
                        category=None,
                        cwe=tuple(row["cwe"].split(" + ")),
                        is_vulnerable=True,
                    )
                )

    return mapping


def load_skims_results() -> Score:
    errors_per_category: Dict[Optional[str], int] = {}
    false_negatives: int = 0
    false_positives: int = 0
    true_negatives: int = 0
    true_positives: int = 0

    skims_findings = load_benchmark_skims_results()
    for test, result in load_benchmark_expected_results().items():
        success: bool = False
        skims_results = skims_findings.get(test, [])

        # We must check skims had said vulnerable against the expected
        # type of vulnerability.
        # It does not make sense to compare different CWE, for instance
        # in some files skims reports F060 Insecure Exceptions, but the
        # expected vulnerability is a buffer overflow.
        # this CWE comparison brings that into the table, so the
        # results are as realistic as possible
        if any(
            skims_result.is_vulnerable and skims_result.shares_cwe_with(result)
            for skims_result in skims_results
        ):
            if result.is_vulnerable:
                success = True
                true_positives += 1
            else:
                false_positives += 1
        else:
            if result.is_vulnerable:
                false_negatives += 1
            else:
                success = True
                true_negatives += 1

        errors_per_category.setdefault(result.category, 0)
        if not success and errors_per_category[result.category] < 3:
            errors_per_category[result.category] += 1
            log_blocking(
                "error",
                "%s, skims: %s, expected: %s",
                test,
                skims_results,
                result,
            )

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
    results_owasp: Dict[str, Any] = {
        "stream": "owasp",
        "record": {},
    }

    for attr, attr_value in (
        ("false_negatives", score.false_negatives),
        ("false_positives", score.false_positives),
        ("true_negatives", score.true_negatives),
        ("true_positives", score.true_positives),
        ("true_positives_rate", score.true_positives_rate),
        ("false_positives_rate", score.false_positives_rate),
        ("score", 100 * score.score),
    ):
        results_owasp["record"][attr] = attr_value
        log_blocking("info", "%s: %s", attr, attr_value)

    with open("benchmark.json", "w", encoding="utf-8") as handle:
        json.dump(results_owasp, handle, sort_keys=True)


if __name__ == "__main__":
    main()
