# Standard libraries
from collections import defaultdict
from typing import (
    Dict,
    List
)

# Third party libraries
from aiodataloader import DataLoader
from aioextensions import collect

# Local libraries
from backend.domain import tag as tag_domain
from backend.typing import Tag as TagType


async def _batch_load_fn(organization_names: List[str]) -> List[List[TagType]]:
    tags: Dict[str, List[TagType]] = defaultdict(List[TagType])
    organizations_tags = await collect(
        tag_domain.get_tags(organization_name)
        for organization_name in organization_names
    )

    for index, organization_tags in enumerate(organizations_tags):
        organization_name = organization_names[index]
        tags[organization_name] = [
            dict(
                last_closing_date=tag['last_closing_date'],
                max_open_severity=tag['max_open_severity'],
                max_severity=tag['max_severity'],
                mean_remediate=tag['mean_remediate'],
                mean_remediate_critical_severity=tag[
                    'mean_remediate_critical_severity'
                ],
                mean_remediate_low_severity=tag[
                    'mean_remediate_low_severity'
                ],
                mean_remediate_high_severity=tag[
                    'mean_remediate_high_severity'
                ],
                mean_remediate_medium_severity=tag[
                    'mean_remediate_medium_severity'
                ],
                organization=organization_name,
                projects=tag['projects'],
                tag=tag['tag'],
            )
            for tag in organization_tags
        ]

    return [
        tags.get(organization_name, [])
        for organization_name in organization_names
    ]


# pylint: disable=too-few-public-methods
class OrganizationTagsLoader(DataLoader):  # type: ignore
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self,
        organization_names: List[str]
    ) -> List[List[TagType]]:
        return await _batch_load_fn(organization_names)
