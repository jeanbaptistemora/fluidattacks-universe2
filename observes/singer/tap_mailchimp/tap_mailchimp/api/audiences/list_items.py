# Standard libraries
from functools import (
    partial,
)
from typing import (
    Dict,
    Iterator,
)

# Third party libraries

# Local libraries
from tap_mailchimp.api.common import (
    list_items,
)
from tap_mailchimp.api.common.raw import (
    AbsReportId,
    AudienceId,
    GrowthHistId,
    InterestCatgId,
    MemberId,
    RawSource,
)


def list_audiences(
    raw_source: RawSource,
) -> Iterator[AudienceId]:
    return list_items(
        raw_source.list_audiences,
        'lists',
        lambda item: AudienceId(item['id'])
    )


def list_abuse_reports(
    raw_source: RawSource,
    audience: AudienceId,
) -> Iterator[AbsReportId]:
    def id_builder(item: Dict[str, str]) -> AbsReportId:
        return AbsReportId(
            audience_id=audience,
            str_id=item['id']
        )

    return list_items(
        partial(raw_source.list_abuse_reports, audience),
        'abuse_reports',
        id_builder
    )


def list_members(
    raw_source: RawSource,
    audience: AudienceId,
) -> Iterator[MemberId]:
    def id_builder(item: Dict[str, str]) -> MemberId:
        return MemberId(
            audience_id=audience,
            str_id=item['id']
        )

    return list_items(
        partial(raw_source.list_members, audience),
        'members',
        id_builder
    )


def list_growth_hist(
    raw_source: RawSource,
    audience: AudienceId,
) -> Iterator[GrowthHistId]:
    def id_builder(item: Dict[str, str]) -> GrowthHistId:
        return GrowthHistId(
            audience_id=audience,
            str_id=item['month']
        )

    return list_items(
        partial(raw_source.list_growth_hist, audience),
        'history',
        id_builder
    )


def list_interest_catg(
    raw_source: RawSource,
    audience: AudienceId,
) -> Iterator[InterestCatgId]:
    def id_builder(item: Dict[str, str]) -> InterestCatgId:
        return InterestCatgId(
            audience_id=audience,
            str_id=item['id']
        )

    return list_items(
        partial(raw_source.list_interest_catg, audience),
        'categories',
        id_builder
    )
