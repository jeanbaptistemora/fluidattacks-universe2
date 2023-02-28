from collections.abc import (
    Iterable,
)
from db_model.groups.enums import (
    GroupManaged,
    GroupStateStatus,
)
from db_model.groups.types import (
    Group,
)


def exclude_review_groups(groups: Iterable[Group]) -> list[Group]:
    return [
        group
        for group in groups
        if group.state.managed != GroupManaged.UNDER_REVIEW
    ]


def filter_trial_groups(groups: Iterable[Group]) -> list[Group]:
    return [
        group
        for group in groups
        if group.state.managed
        in {GroupManaged.TRIAL, GroupManaged.UNDER_REVIEW}
    ]


def filter_active_groups(groups: Iterable[Group]) -> list[Group]:
    return [
        group
        for group in groups
        if group.state.status == GroupStateStatus.ACTIVE
    ]


def filter_deleted_groups(groups: Iterable[Group]) -> list[Group]:
    return [
        group
        for group in groups
        if group.state.status == GroupStateStatus.DELETED
    ]
