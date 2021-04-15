# Standard libraries
from __future__ import (
    annotations,
)
from typing import (
    NamedTuple,
)

# Third party libraries
from delighted import (
    Client,
    HTTPAdapter,
)

# Local libraries
from tap_delighted.auth import (
    Credentials,
)
from tap_delighted.api.metrics import (
    MetricsApi,
)
from tap_delighted.api.people import (
    BouncedPage,
    PeopleApi,
    UnsubscribedPage,
)
from tap_delighted.api.survey import (
    SurveyApi,
    SurveyPage,
)


class ApiClient(NamedTuple):
    metrics: MetricsApi
    people: PeopleApi
    survey: SurveyApi

    @classmethod
    def new(cls, creds: Credentials) -> ApiClient:
        client = Client(
            api_key=creds.api_key,
            api_base_url='https://api.delighted.com/v1/',
            http_adapter=HTTPAdapter()
        )
        return cls(
            metrics=MetricsApi.new(client),
            people=PeopleApi.new(client),
            survey=SurveyApi.new(client),
        )


__all__ = [
    'BouncedPage',
    'SurveyPage',
    'UnsubscribedPage',
]
