from functools import (
    partial,
)
from singer_io.singer2.json import (
    JsonObj,
)
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
from typing import (
    Iterator,
)


def list_audiences(
    raw_source: RawSource,
) -> Iterator[AudienceId]:
    return list_items(
        raw_source.list_audiences,
        "lists",
        lambda item: AudienceId(item["id"].to_primitive(str)),
    )


def list_abuse_reports(
    raw_source: RawSource,
    audience: AudienceId,
) -> Iterator[AbsReportId]:
    def id_builder(item: JsonObj) -> AbsReportId:
        return AbsReportId(audience, item["id"].to_primitive(int))

    return list_items(
        partial(raw_source.list_abuse_reports, audience),
        "abuse_reports",
        id_builder,
    )


def list_members(
    raw_source: RawSource,
    audience: AudienceId,
) -> Iterator[MemberId]:
    def id_builder(item: JsonObj) -> MemberId:
        return MemberId(audience, item["id"].to_primitive(str))

    return list_items(
        partial(raw_source.list_members, audience), "members", id_builder
    )


def list_growth_hist(
    raw_source: RawSource,
    audience: AudienceId,
) -> Iterator[GrowthHistId]:
    def id_builder(item: JsonObj) -> GrowthHistId:
        return GrowthHistId(audience, item["month"].to_primitive(str))

    return list_items(
        partial(raw_source.list_growth_hist, audience), "history", id_builder
    )


def list_interest_catg(
    raw_source: RawSource,
    audience: AudienceId,
) -> Iterator[InterestCatgId]:
    def id_builder(item: JsonObj) -> InterestCatgId:
        return InterestCatgId(audience, item["id"].to_primitive(str))

    return list_items(
        partial(raw_source.list_interest_catg, audience),
        "categories",
        id_builder,
    )
