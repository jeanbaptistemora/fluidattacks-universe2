# Standard libraries
import math
from itertools import (
    chain,
)
from typing import (
    Callable,
    Iterator,
)

# Third party libraries

# Local libraries
import paginator
from paginator import (
    PageId,
)
from tap_mailchimp.api.common import (
    api_data,
    list_items_alert,
)
from tap_mailchimp.api.common.api_data import (
    ApiData,
)
from tap_mailchimp.api.common.raw import (
    AbsReportId,
    AudienceId,
    GrowthHistId,
    InterestCatgId,
    MemberId,
    RawSource,
)


MAX_PER_PAGE = 1000


class NoneTotal(Exception):
    pass


def list_audiences(
    raw_source: RawSource,
) -> Iterator[AudienceId]:
    getter: Callable[[PageId], ApiData] = (
        lambda page: api_data.create_api_data(
            raw_source.list_audiences(page)
        )
    )
    test_page = getter(PageId(page=0, per_page=1))
    chunk_size = MAX_PER_PAGE
    if test_page.total_items is None:
        raise NoneTotal()
    total_pages = math.ceil(test_page.total_items / chunk_size)
    pages = paginator.new_page_range(range(total_pages), chunk_size)
    results: Iterator[ApiData] = paginator.get_pages(pages, getter)

    def extract_aud_ids(a_data: ApiData) -> Iterator[AudienceId]:
        audiences_data = a_data.data['lists']
        return iter(map(lambda a: AudienceId(a['id']), audiences_data))

    return chain.from_iterable(map(extract_aud_ids, results))


def list_abuse_reports(
    raw_source: RawSource,
    audience: AudienceId,
) -> Iterator[AbsReportId]:
    result = api_data.create_api_data(
        raw_source.list_abuse_reports(audience)
    )
    list_items_alert(
        f'list_abuse_reports {audience}',
        result.total_items
    )
    data = result.data['abuse_reports']
    return iter(map(
        lambda item: AbsReportId(
            audience_id=audience,
            str_id=item['id']
        ),
        data
    ))


def list_members(
    raw_source: RawSource,
    audience: AudienceId,
) -> Iterator[MemberId]:
    result = api_data.create_api_data(
        raw_source.list_members(audience)
    )
    list_items_alert(
        f'list_members {audience}',
        result.total_items
    )
    data = result.data['members']
    return iter(map(
        lambda item: MemberId(
            audience_id=audience,
            str_id=item['id']
        ),
        data
    ))


def list_growth_hist(
    raw_source: RawSource,
    audience: AudienceId,
) -> Iterator[GrowthHistId]:
    result = api_data.create_api_data(
        raw_source.list_growth_hist(audience)
    )
    list_items_alert(
        f'list_growth_hist {audience}',
        result.total_items
    )
    data = result.data['history']
    return iter(map(
        lambda item: GrowthHistId(
            audience_id=audience,
            str_id=item['month']
        ),
        data
    ))


def list_interest_catg(
    raw_source: RawSource,
    audience: AudienceId,
) -> Iterator[InterestCatgId]:
    result = api_data.create_api_data(
        raw_source.list_interest_catg(audience)
    )
    list_items_alert(
        f'list_interest_catg {audience}',
        result.total_items
    )
    data = result.data['categories']
    return iter(map(
        lambda item: InterestCatgId(
            audience_id=audience,
            str_id=item['id']
        ),
        data
    ))
