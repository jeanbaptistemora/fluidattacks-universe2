import json
import os
import sys
from typing import (
    Any,
)


def error(msg: str) -> None:
    print("[ERROR]", msg)


def test_schedule_maintainers(*, name: str, values: Any) -> bool:
    success: bool = True

    if len(values["meta"]["maintainers"]) == 0:
        success = False
        error(
            "'meta.maintainers' option"
            " must not be empty"
            f" in schedule '{name}'."
        )

    return success


def test_schedule(*, name: str, values: Any) -> bool:
    return all(
        tuple(
            [
                test_meta_description(name=name, values=values),
                test_meta_required_by(name=name, values=values),
            ]
        )
    )


def test_meta_description(*, name: str, values: Any) -> bool:
    success: bool = True
    min_chars: int = 50
    description: str = values["meta"]["description"]

    if len(description) < min_chars:
        success = False
        error(
            "'meta.description' option"
            f" must be at least {min_chars} characters long"
            f" in schedule '{name}'."
        )

    return success


def test_meta_required_by(*, name: str, values: Any) -> bool:
    success: bool = True
    required_by: list[str] = values["meta"]["requiredBy"]

    if len(required_by) == 0:
        success = False
        error(
            "'meta.requiredBy' option"
            f"must must not be empty in schedule '{name}'."
        )

    return success


def main() -> None:
    success: bool = True
    data: dict[str, Any] = json.loads(os.environ["DATA"])

    success = success and all(
        tuple(
            test_schedule_maintainers(name=name, values=values)
            for (name, values) in data.items()
        )
    )

    success = success and all(
        tuple(
            test_schedule(name=name, values=values)
            for (name, values) in data.items()
            if os.environ["CI_COMMIT_REF_NAME"]
            in values["meta"]["maintainers"]
        )
    )

    sys.exit(0 if success else 1)


main()
