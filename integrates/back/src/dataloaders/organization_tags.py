from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
)
from collections import (
    defaultdict,
)
from custom_types import (
    Tag as TagType,
)
from newutils.utils import (
    get_key_or_fallback,
)
from tags import (
    domain as tags_domain,
)
from typing import (
    Dict,
    List,
)


async def _batch_load_fn(organization_names: List[str]) -> List[List[TagType]]:
    tags: Dict[str, List[TagType]] = defaultdict(List[TagType])
    organizations_tags = await collect(
        tags_domain.get_tags(organization_name)
        for organization_name in organization_names
    )

    for index, organization_tags in enumerate(organizations_tags):
        organization_name = organization_names[index]
        tags[organization_name] = [
            dict(
                last_closing_date=tag["last_closing_date"],
                max_open_severity=tag["max_open_severity"],
                max_severity=tag["max_severity"],
                mean_remediate=tag["mean_remediate"],
                mean_remediate_critical_severity=tag[
                    "mean_remediate_critical_severity"
                ],
                mean_remediate_low_severity=tag["mean_remediate_low_severity"],
                mean_remediate_high_severity=tag[
                    "mean_remediate_high_severity"
                ],
                mean_remediate_medium_severity=tag[
                    "mean_remediate_medium_severity"
                ],
                organization=organization_name,
                tag=tag["tag"],
                projects=sorted(
                    get_key_or_fallback(tag, "groups", "projects")
                ),
                # Standardization field
                groups=sorted(get_key_or_fallback(tag, "groups", "projects")),
            )
            for tag in organization_tags
        ]
    return [
        tags.get(organization_name, [])
        for organization_name in organization_names
    ]


class OrganizationTagsLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, organization_names: List[str]
    ) -> List[List[TagType]]:
        return await _batch_load_fn(organization_names)
