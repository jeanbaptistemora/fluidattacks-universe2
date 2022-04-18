from __future__ import (
    annotations,
)

from delighted import (
    Client,
    HTTPAdapter,
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
from tap_delighted.auth import (
    Credentials,
)
from typing import (
    NamedTuple,
    TypeVar,
)

ApiPage = TypeVar("ApiPage", BouncedPage, SurveyPage, UnsubscribedPage)


class ApiClient(NamedTuple):
    metrics: MetricsApi
    people: PeopleApi
    survey: SurveyApi

    @classmethod
    def new(cls, creds: Credentials) -> ApiClient:
        client = Client(
            api_key=creds.api_key,
            api_base_url="https://api.delighted.com/v1/",
            http_adapter=HTTPAdapter(),
        )
        return cls(
            metrics=MetricsApi.new(client),
            people=PeopleApi.new(client),
            survey=SurveyApi.new(client),
        )


__all__ = [
    "BouncedPage",
    "SurveyPage",
    "UnsubscribedPage",
]
