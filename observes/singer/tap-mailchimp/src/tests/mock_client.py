from paginator import (
    PageId,
)
from singer_io.singer2.json import (
    JsonFactory,
    JsonObj,
)
from tap_mailchimp import (
    api,
)
from tap_mailchimp.api import (
    ApiClient,
    AudienceId,
)
from tap_mailchimp.api.common.raw import (
    RawSource,
)


def _list_audiences(_page: PageId) -> JsonObj:
    with open("./tests/mock_data/audience.json", encoding="UTF-8") as data:
        return JsonFactory.load(data)["list_audiences"].to_json()


def _get_audience(audience: AudienceId) -> JsonObj:
    with open("./tests/mock_data/audience.json", encoding="UTF-8") as data:
        return (
            JsonFactory.load(data)["get_audience"]
            .to_json()[audience.item_id]
            .to_json()
        )


def mock_data_source() -> RawSource:
    return RawSource(
        list_audiences=_list_audiences,
        get_audience=_get_audience,
        list_abuse_reports=lambda x: x,  # type: ignore
        get_abuse_report=lambda x: x,  # type: ignore
        get_activity=lambda x: x,  # type: ignore
        get_top_clients=lambda x: x,  # type: ignore
        list_members=lambda x: x,  # type: ignore
        get_member=lambda x: x,  # type: ignore
        list_growth_hist=lambda x: x,  # type: ignore
        get_growth_hist=lambda x: x,  # type: ignore
        list_interest_catg=lambda x: x,  # type: ignore
        get_interest_catg=lambda x: x,  # type: ignore
        get_audience_locations=lambda x: x,  # type: ignore
        list_campaigns=lambda x: x,  # type: ignore
        get_campaign=lambda x: x,  # type: ignore
        list_feedbacks=lambda x: x,  # type: ignore
        get_feedback=lambda x: x,  # type: ignore
        get_checklist=lambda x: x,  # type: ignore
    )


def new_client() -> ApiClient:
    return api.new_client_from_source(mock_data_source())
