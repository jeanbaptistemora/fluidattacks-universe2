import json
import os
import sys
from typing import (
    Any,
)


def test_meta_keys(*, name: str, values: Any) -> bool:
    success: bool = False
    keys: list[str] = [
        "description",
        "requiredBy",
        "responsible",
        "lastReviewed",
    ]

    if "meta" not in values.keys():
        print(f"[ERROR] 'meta' option does not exist in schedule '{name}'.")
    else:
        success = True

    if success:
        for key in keys:
            if key not in values["meta"].keys():
                print(
                    f"[ERROR] 'meta.{key}' option"
                    f" does not exist in schedule '{name}'."
                )
                success = False

    return success


def main() -> None:
    success: bool = False
    schedules: dict[str, Any] = json.loads(os.environ["SCHEDULES"])

    success = all(
        tuple(
            test_meta_keys(name=name, values=values)
            for (name, values) in schedules.items()
        )
    )

    sys.exit(0 if success else 1)


main()
