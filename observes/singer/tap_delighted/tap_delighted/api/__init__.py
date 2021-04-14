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
from tap_delighted.api.survey import (
    SurveyApi,
    SurveyPage,
)
from tap_delighted.api.people import (
    PeopleApi,
    BouncedPage,
)


class ApiClient(NamedTuple):
    survey: SurveyApi
    people: PeopleApi

    @classmethod
    def new(cls, creds: Credentials) -> ApiClient:
        client = Client(
            api_key=creds.api_key,
            api_base_url='https://api.delighted.com/v1/',
            http_adapter=HTTPAdapter()
        )
        return cls(
            survey=SurveyApi.new(client),
            people=PeopleApi.new(client),
        )


__all__ = [
    'SurveyPage',
    'BouncedPage'
]
