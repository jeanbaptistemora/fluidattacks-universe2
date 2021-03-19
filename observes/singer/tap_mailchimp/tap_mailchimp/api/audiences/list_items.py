# Standard libraries
from typing import (
    Iterator,
)

# Third party libraries

# Local libraries
import utils_logger
from tap_mailchimp.api.common import (
    api_data,
)
from tap_mailchimp.api.common.raw import (
    AbsReportId,
    AudienceId,
    GrowthHistId,
    InterestCatgId,
    MemberId,
    RawSource,
)

LOG = utils_logger.get_log(__name__)


def list_audiences(
    raw_source: RawSource,
) -> Iterator[AudienceId]:
    result = api_data.create_api_data(
        raw_source.list_audiences()
    )
    audiences_data = result.data['lists']
    return iter(map(lambda a: AudienceId(a['id']), audiences_data))


def list_abuse_reports(
    raw_source: RawSource,
    audience: AudienceId
) -> Iterator[AbsReportId]:
    result = api_data.create_api_data(
        raw_source.list_abuse_reports(audience)
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
    audience: AudienceId
) -> Iterator[MemberId]:
    result = api_data.create_api_data(
        raw_source.list_members(audience)
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
    audience: AudienceId
) -> Iterator[GrowthHistId]:
    result = api_data.create_api_data(
        raw_source.list_growth_hist(audience)
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
    audience: AudienceId
) -> Iterator[InterestCatgId]:
    result = api_data.create_api_data(
        raw_source.list_interest_catg(audience)
    )
    LOG.debug('list_interest_catg result: %s', result)
    data = result.data['categories']
    return iter(map(
        lambda item: InterestCatgId(
            audience_id=audience,
            str_id=item['id']
        ),
        data
    ))
