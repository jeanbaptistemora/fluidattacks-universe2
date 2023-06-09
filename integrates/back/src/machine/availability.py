from datetime import (
    datetime,
    timedelta,
    timezone,
)
from db_model.enums import (
    Source,
)
from enum import (
    Enum,
)
import holidays
import json
from machine.jobs import (
    get_finding_code_from_title,
)
from newutils import (
    requests as requests_utils,
)
from newutils.env import (
    guess_environment,
)
import os
from typing import (
    Any,
)


def _json_load(path: str) -> Any:
    with open(path, encoding="utf-8") as file:
        return json.load(file)


QUEUES: dict[str, dict[str, str]] = _json_load(os.environ["MACHINE_QUEUES"])


class AvailabilityEnum(str, Enum):
    ALWAYS: str = "ALWAYS"
    NEVER: str = "NEVER"
    WORKING_HOURS: str = "WORKING_HOURS"

    def is_available_right_now(self) -> bool:
        now: datetime = datetime.now(timezone(timedelta(hours=-5)))  # Colombia

        if self == AvailabilityEnum.ALWAYS:
            return True
        if self == AvailabilityEnum.NEVER:
            return False
        if self == AvailabilityEnum.WORKING_HOURS:
            if guess_environment() == "production":
                in_working_days: bool = (
                    0 <= now.weekday() <= 5
                )  # Monday to Friday
                in_working_hours: bool = (
                    9 <= now.hour < 16
                )  # [9:00, 15:59] Col
                is_holiday: bool = now.strftime("%y-%m-%d") in holidays.CO()
                return in_working_days and in_working_hours and not is_holiday
            return True
        raise NotImplementedError()


def is_check_available(finding_code: str) -> bool:
    for data in QUEUES.values():
        if finding_code in data["findings"]:
            return AvailabilityEnum(
                data["availability"]
            ).is_available_right_now()

    raise NotImplementedError(f"{finding_code} does not belong to a queue")


def operation_can_be_executed(context: Any, finding_title: str) -> bool:
    source = requests_utils.get_source_new(context)
    if source.value == Source.MACHINE.value and (
        finding_code := get_finding_code_from_title(finding_title)
    ):
        return is_check_available(finding_code)
    return True


def get_available_queues() -> dict[str, dict[str, str]]:
    return {
        queue: data
        for queue, data in QUEUES.items()
        if AvailabilityEnum(data["availability"]).is_available_right_now()
    }


def print_available_queues() -> None:
    print(json.dumps(get_available_queues(), indent=2, sort_keys=True))
