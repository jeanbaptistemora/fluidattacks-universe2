from datetime import (
    datetime,
)
from dateutil.relativedelta import (
    relativedelta,
)
import json
import os
import sys
from typing import (
    Any,
)


def error(msg: str) -> None:
    print("[ERROR]", msg)


def test_schedule(*, name: str, values: Any) -> bool:
    return all(
        tuple(
            [
                test_meta_last_reviewed(name=name, values=values),
            ]
        )
    )


def test_meta_last_reviewed(*, name: str, values: Any) -> bool:
    success: bool = True
    delta_months: int = 1
    time_format: str = "%d-%m-%Y"
    last_reviewed: datetime = datetime.strptime(
        values["meta"]["lastReviewed"],
        time_format,
    )
    next_review: datetime = last_reviewed + relativedelta(months=delta_months)
    today: datetime = datetime.today()

    if today > next_review:
        success = False
        error(
            f"{name}.meta.lastReviewed was on"
            f" {last_reviewed.strftime(time_format)}."
            " Please review and update the schedule."
        )

    return success


def main() -> None:
    data: dict[str, Any] = json.loads(os.environ["DATA"])
    user: str = os.environ["CI_COMMIT_REF_NAME"].removesuffix("atfluid")

    success: bool = all(
        tuple(
            test_schedule(name=name, values=values)
            for (name, values) in data.items()
            if user in values["meta"]["maintainers"]
        )
    )

    sys.exit(0 if success else 1)


main()
