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
)

# Local libraries
from tap_delighted.api.survey import (
    SurveyApi,
)


class ApiClient(NamedTuple):
    survey: SurveyApi

    @classmethod
    def new(cls, client: Client) -> ApiClient:
        return cls(
            survey=SurveyApi.new(client)
        )
