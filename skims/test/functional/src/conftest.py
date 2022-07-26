import pytest
from typing import (
    Any,
    Dict,
)


@pytest.fixture(autouse=True, scope="session")
def generic_data() -> Dict[str, Any]:
    org_id = "59e95b33-59b3-4d10-b2a5-a0729ad79aad"
    jti = "8e2d8d26f77df34b96fce567a1b7f232d838c4bfc94872f24e1e602507c1f939"
    salt = "3b3e42b6eff02ab9da367b294e502ba7ba982bb86b3fe8ce98133410522a3863"
    return {
        "organizations": [
            {
                "pk": "ORG#" + org_id,
                "sk": "ORG#esdeath",
                "pk_2": "ORG#all",
                "sk_2": "ORG#" + org_id,
                "id": org_id,
                "name": "esdeath",
                "policies": {
                    "modified_by": "unknown",
                    "modified_date": "2022-06-09T19:36:16+00:00",
                },
                "state": {
                    "modified_by": "customer@domain.com",
                    "modified_date": "2022-05-12T00:17:09+00:00",
                    "status": "ACTIVE",
                },
            },
            {
                "pk": "ORG#" + org_id,
                "sk": "POLICIES#2022-06-09T19:36:16+00:00",
                "modified_by": "unknown",
                "modified_date": "2022-06-09T19:36:16+00:00",
            },
            {
                "pk": "ORG#" + org_id,
                "sk": "STATE#2022-05-12T00:17:09+00:00",
                "modified_by": "customer@domain.com",
                "modified_date": "2022-05-12T00:17:09+00:00",
                "status": "ACTIVE",
            },
        ],
        "groups": [
            {
                "pk": "GROUP#jessup",
                "sk": "ORG#" + org_id,
                "description": "Skims functional tests group",
                "language": "EN",
                "name": "jessup",
                "organization_id": org_id,
                "sprint_start_date": "2022-06-06T00:00:00",
                "sprint_duration": "1",
                "state": {
                    "pk": "ORG#" + org_id,
                    "sk": "STATE#2022-05-12T00:47:02+00:00",
                    "has_machine": "true",
                    "has_squad": "true",
                    "managed": "true",
                    "modified_by": "customer@domain.com",
                    "modified_date": "2022-05-12T00:47:02+00:00",
                    "status": "ACTIVE",
                    "tier": "SQUAD",
                    "type": "CONTINUOUS",
                },
            },
            {
                "pk": "GROUP#jessup",
                "sk": "STATE#2022-05-12T00:47:02+00:00",
                "has_machine": "true",
                "has_squad": "true",
                "managed": "true",
                "modified_by": "customer@domain.com",
                "modified_date": "2022-05-12T00:47:02+00:00",
                "status": "ACTIVE",
                "tier": "SQUAD",
                "type": "CONTINUOUS",
            },
        ],
        "stakeholders": [
            {
                "pk": "USER#machine@fluidattacks.com",
                "sk": "USER#machine@fluidattacks.com",
                "pk_2": "USER#all",
                "sk_2": "USER#machine@fluidattacks.com",
                "email": "machine@fluidattacks.com",
                "first_name": "Machine",
                "last_name": "Services",
                "is_registered": "True",
                "last_login_date": "2022-05-11T23:52:26+00:00",
                "registration_date": "2022-05-11T23:52:26+00:00",
                "access_token": {
                    "iat": "1652323789",
                    "jti": jti,
                    "salt": salt,
                },
            },
        ],
    }
