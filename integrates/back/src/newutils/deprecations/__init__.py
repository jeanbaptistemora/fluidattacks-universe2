# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

"""
    This newutils package houses the schema deprecation parsing and filters to
    find out and report overdue fields in the schema and gather the needed info
    to send deprecation notices
"""
from newutils.deprecations.ast import (
    get_deprecations_by_period,
    get_due_date,
)
from newutils.deprecations.filters import (
    filter_api_deprecation_dict,
    filter_api_deprecation_list,
)
from newutils.deprecations.types import (
    ApiDeprecation,
    ApiFieldType,
)

__all__ = [
    "ApiDeprecation",
    "ApiFieldType",
    "filter_api_deprecation_dict",
    "filter_api_deprecation_list",
    "get_deprecations_by_period",
    "get_due_date",
]
