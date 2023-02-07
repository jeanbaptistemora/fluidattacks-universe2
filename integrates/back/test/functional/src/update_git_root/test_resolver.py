# pylint: disable=import-error
from . import (
    get_git_root,
    get_result_1,
)
from dataloaders import (
    get_new_context,
)
from freezegun import (
    freeze_time,
)
import pytest
from pytest_mock import (
    MockerFixture,
)
from roots import (
    domain as roots_domain,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_git_root")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
    ],
)
@freeze_time("2022-10-21T15:58:31.280182+00:00")
async def test_update_git_root_new_cred(
    populate: bool, email: str, mocker: MockerFixture
) -> None:
    assert populate
    mocker.patch.object(
        roots_domain, "queue_sync_git_roots", return_value=None
    )
    result_group: dict = await get_git_root(
        user=email,
        group="group1",
        root_id="88637616-41d4-4242-854a-db8ff7fe1ab6",
    )
    assert "errors" not in result_group
    assert result_group["data"]["root"] == {
        "createdAt": "2022-02-10T14:58:10+00:00",
        "createdBy": "user_manager@gmail.com",
        "id": "88637616-41d4-4242-854a-db8ff7fe1ab6",
        "lastEditedAt": "2022-02-10T14:58:10+00:00",
        "lastEditedBy": "user_manager@gmail.com",
    }

    credential_key = (
        "LS0tLS1CRUdJTiBPUEVOU1NIIFBSSVZBVEUgS0VZLS0tLS0KYjNCbGJuTnphQzFyWlhr"
        "dGRqRUFBQUFBQ21GbGN6STFOaTFqZEhJQUFBQUdZbU55ZVhCMEFBQUFHQUFBQUJCZjJF"
        "dWFKRgp3dnA4WVpZRWN5aldleUFBQUFFQUFBQUFFQUFBQ1hBQUFBQjNOemFDMXljMkVB"
        "QUFBREFRQUJBQUFBZ1FDZS9rbEt6dEZ1CktKLzdFQjRJZ0lFSCswdzVHT2ZwWHFUaGYr"
        "aEtxd01QZDgyQTl4OTdFbzA0UHo4V0dGdXc3S1FwM3B4NitOU3BOR2dMVGoKeFB6alhO"
        "Q3NNaWJzUjgxNmNWVGVjNVk4STlvQnB0cHFJZWY3cmdpbjhBNG5waCszV1ZKa1U2NEJM"
        "VjNsQWhGem84QTFBOAppWlhDbDA0VXVQVE9mV2oxQlNIdjVRQUFBZ0RHZXBiY3pmcjRF"
        "NWFEb25SeUhZSmNTcXdVbWZCOGdEbFJkdDRjWlFHaE5NCkxtUlFVdlhOaWpnbzFhazBa"
        "akhxaDRIQXdmR1NySGxjdUJKOUlSdWZ1ekhCK2xrd0R6akJBeWR3Z3JJQndCbDNFcXBa"
        "NkgKY1l6U29rZEZ4TFZqVXJPY2RQTTV5SWM3TTB1MFU5WGNuN0ZjYTk0UThLY3I2bXc5"
        "aVQ5ZnlhQURZMnJtMHJ1VTcxUXcvOQo4RHdna3dsNmNBQVVrWnQvR2syaG8vc0FYMUIy"
        "cElVRUFJL2FMcWYzVjBIdWNsN2ZWZGxsYldneWJIS1hIdXlUdEZJN09HCmlOUHBhUy94"
        "dFdsSmcyTmJad09MWUo4MlpQKzlnbzlUM3ZVMTZOTGt3bTUwa04rckRRazk4MC80OGZN"
        "T042RFlKRVo3VUIKWVpoSnZoUS9nYjdwT1JMSmhTT3p4cDFyN3hoamlPSHpid0p0OVlS"
        "aWdHcFBtT28vOEw0bml4TTJqaC9jcjhFc0ZlVGFaVApBOGg3M2RObXVLWkZ4OGJPeTc3"
        "aFQ3YW1GK2xxdm1xSC91M2d5UkcvMnVyVGpBZ1EvOENZYmk3czcwUEVhTzBPRWxTRmQz"
        "CjZWTlFiNjd1amZjWVdkbmxPTG5FSHlWMm9oTG5TbVNJQjBxRnhqaWptelg1K2pVbm82"
        "dnpRTCtOdDA4R01XRVRYbk4vUUYKeENGRDJ1UVMrQ2Q3dngvUnFzNmdVR0JQSTVnMVFT"
        "cG5hV1NKSHlXYlM5WHoyeGJnQ0xnVjA1S0dKQ1hWajZtNnNjc0ZEZQpLVlRxWjRiK1RH"
        "S0NrMjF6WkltOSt2VUx2OWgzbmIxQ0lYN0R2MkJnM0xsczAvOGdLYXFjVUlYejRUVjhi"
        "ZHQwMkZsc2hnCjlaSlpsa25mMlE9PQotLS0tLUVORCBPUEVOU1NIIFBSSVZBVEUgS0VZ"
        "LS0tLS0="
    )
    cred_new_name = "New SSH Key"
    group_name: str = "group1"
    organization_id: str = "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db"
    result: dict = await get_result_1(
        user=email,
        group=group_name,
        credential_key=credential_key,
        credential_name=cred_new_name,
    )
    assert "errors" not in result
    assert result["data"]["updateGitRoot"]["success"]

    loaders = get_new_context()
    credentials = await loaders.organization_credentials.load(organization_id)
    credential_names = [credential.state.name for credential in credentials]
    assert cred_new_name in credential_names

    result_group = await get_git_root(
        user=email,
        group="group1",
        root_id="88637616-41d4-4242-854a-db8ff7fe1ab6",
    )
    assert "errors" not in result_group
    assert result_group["data"]["root"] == {
        "createdAt": "2022-02-10T14:58:10+00:00",
        "createdBy": "user_manager@gmail.com",
        "id": "88637616-41d4-4242-854a-db8ff7fe1ab6",
        "lastEditedAt": "2022-10-21T15:58:31.280182+00:00",
        "lastEditedBy": email,
    }
