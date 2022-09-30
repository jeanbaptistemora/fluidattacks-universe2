# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0


from .types import (
    ComplianceStandard,
    ComplianceUnreliableIndicators,
)
from dynamodb.types import (
    Item,
)


def format_compliance_standard(item: Item) -> ComplianceStandard:
    return ComplianceStandard(
        avg_organization_compliance_level=item[
            "avg_organization_compliance_level"
        ],
        best_organization_compliance_level=item[
            "best_organization_compliance_level"
        ],
        standard_name=item["standard_name"],
        worst_organization_compliance_level=item[
            "worst_organization_compliance_level"
        ],
    )


def format_compliance_standard_item(
    standard: ComplianceStandard,
) -> Item:
    return {
        "avg_organization_compliance_level": (
            standard.avg_organization_compliance_level
        ),
        "best_organization_compliance_level": (
            standard.best_organization_compliance_level
        ),
        "standard_name": standard.standard_name,
        "worst_organization_compliance_level": (
            standard.worst_organization_compliance_level
        ),
    }


def format_unreliable_indicators(
    item: Item,
) -> ComplianceUnreliableIndicators:
    return ComplianceUnreliableIndicators(
        standards=[
            format_compliance_standard(standard_compliance)
            for standard_compliance in item["standards"]
        ]
        if "standards" in item
        else None,
    )


def format_unreliable_indicators_item(
    indicators: ComplianceUnreliableIndicators,
) -> Item:
    return {
        "standards": [
            format_compliance_standard_item(standard)
            for standard in indicators.standards
        ]
        if indicators.standards is not None
        else None,
    }
