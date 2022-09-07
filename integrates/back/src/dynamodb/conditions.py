# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from boto3.dynamodb.conditions import (
    Attr,
    ConditionBase,
)
from typing import (
    Any,
    Optional,
)


def get_filter_expression(filters: dict[str, Any]) -> Optional[ConditionBase]:
    """Returns a filter expression from a key-value input"""
    filter_expression = None

    for filter_attribute, filter_value in filters.items():
        if filter_value is not None:
            attribute = filter_attribute.replace("_", ".")
            condition = Attr(attribute).contains(filter_value)

            if filter_expression is None:
                filter_expression = condition
            else:
                filter_expression &= condition

    return filter_expression
