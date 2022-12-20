import authz
from authz.enforcer import (
    get_organization_level_enforcer,
)
from authz.model import (
    get_organization_level_roles_model,
)
from dataloaders import (
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model import (
    stakeholders as stakeholders_model,
)
from db_model.groups.enums import (
    GroupLanguage,
    GroupManaged,
    GroupService,
    GroupStateStatus,
    GroupSubscriptionType,
    GroupTier,
)
from db_model.groups.types import (
    Group,
    GroupState,
)
from db_model.types import (
    Policies,
)
from decimal import (
    Decimal,
)
from mypy_boto3_dynamodb import (
    DynamoDBServiceResource as ServiceResource,
)
import pytest
from typing import (
    Any,
)
from unittest import (
    mock,
)
from unittest.mock import (
    AsyncMock,
)

# Constants
pytestmark = [
    pytest.mark.asyncio,
]

TABLE_NAME = "integrates_vms"


# pylint: disable=consider-using-dict-items
@mock.patch(
    "dynamodb.operations.get_table_resource",
    new_callable=AsyncMock,
)
@mock.patch(
    "dynamodb.operations.get_resource",
    new_callable=AsyncMock,
)
@pytest.mark.parametrize(
    ["email", "organization_id", "role"],
    [
        [
            "integrates@fluidattacks.com",
            "ORG#f2e2777d-a168-4bea-93cd-d79142b294d2",
            "admin",
        ],
        [
            "integratesuser@gmail.com",
            "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
            "user_manager",
        ],
        [
            "unittesting@fluidattacks.com",
            "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
            "user",
        ],
        [
            "unittesting@gmail.com",
            "ORG#f2e2777d-a168-4bea-93cd-d79142b294d2",
            "admin",
        ],
    ],
)
async def test_organization_level_enforcer(
    # pylint: disable=too-many-arguments
    mock_resource: AsyncMock,
    mock_table_resource: AsyncMock,
    email: str,
    organization_id: str,
    role: str,
    dynamo_resource: ServiceResource,
) -> None:
    def mock_batch_get_item(**kwargs: Any) -> Any:
        return dynamo_resource.batch_get_item(**kwargs)

    def mock_query(**kwargs: Any) -> Any:
        return dynamo_resource.Table(TABLE_NAME).query(**kwargs)

    model = get_organization_level_roles_model(email)
    mock_table_resource.return_value.query.side_effect = mock_query
    mock_resource.return_value.batch_get_item.side_effect = mock_batch_get_item
    enforcer = await get_organization_level_enforcer(get_new_context(), email)
    for action in model[role]["actions"]:
        assert enforcer(
            organization_id, action
        ), f"{role} should be able to do {action}"
    for other_role in model:
        for action in model[other_role]["actions"] - model[role]["actions"]:
            assert not enforcer(
                organization_id, action
            ), f"{role} should not be able to do {action}"


# pylint: disable=consider-using-dict-items
@mock.patch(
    "dynamodb.operations.get_table_resource",
    new_callable=AsyncMock,
)
@mock.patch(
    "dynamodb.operations.get_resource",
    new_callable=AsyncMock,
)
@pytest.mark.parametrize(
    ["subject", "group", "role"],
    [
        [
            "integrates@fluidattacks.com",
            "unittesting",
            "admin",
        ],
        [
            "integratesuser@gmail.com",
            "unittesting",
            "user_manager",
        ],
        [
            "integrateshacker@fluidattacks.com",
            "unittesting",
            "hacker",
        ],
        [
            "continuoushacking@gmail.com",
            "oneshottest",
            "user_manager",
        ],
        [
            "integrateshacker@fluidattacks.com",
            "oneshottest",
            "reattacker",
        ],
        [
            "integratesuser@gmail.com",
            "oneshottest",
            "user",
        ],
    ],
)
@pytest.mark.changes_db
async def test_get_group_level_enforcer(
    # pylint: disable=too-many-arguments
    mock_resource: AsyncMock,
    mock_table_resource: AsyncMock,
    subject: str,
    group: str,
    role: str,
    dynamo_resource: ServiceResource,
) -> None:
    def mock_batch_get_item(**kwargs: Any) -> Any:
        return dynamo_resource.batch_get_item(**kwargs)

    def mock_query(**kwargs: Any) -> Any:
        return dynamo_resource.Table(TABLE_NAME).query(**kwargs)

    model = authz.get_group_level_roles_model(subject)
    mock_table_resource.return_value.query.side_effect = mock_query
    mock_resource.return_value.batch_get_item.side_effect = mock_batch_get_item
    enforcer = await authz.get_group_level_enforcer(get_new_context(), subject)
    for action in model[role]["actions"]:
        assert enforcer(group, action), f"{role} should be able to do {action}"
    for other_role in model:
        for action in model[other_role]["actions"] - model[role]["actions"]:
            assert not enforcer(
                group, action
            ), f"{role} should not be able to do {action}"
    assert mock_table_resource.called is True
    assert mock_resource.called is True


# pylint: disable=consider-using-dict-items
@pytest.mark.changes_db
async def test_user_level_enforcer() -> None:
    test_cases = [
        # Common user
        "test@tests.com",
        # Fluid user
        "test@fluidattacks.com",
    ]
    for subject in test_cases:
        model = authz.get_user_level_roles_model(subject)

        for role in model:
            await stakeholders_model.remove(email=subject)
            await authz.grant_user_level_role(subject, role)
            enforcer = await authz.get_user_level_enforcer(
                get_new_context(), subject
            )

            for action in model[role]["actions"]:
                assert enforcer(
                    action
                ), f"{role} should be able to do {action}"

            for other_role in model:
                for action in (
                    model[other_role]["actions"] - model[role]["actions"]
                ):
                    assert not enforcer(
                        action
                    ), f"{role} should not be able to do {action}"


@pytest.mark.parametrize(
    ["group", "attributes", "results"],
    [
        [
            Group(
                business_name="Testing Company and Sons",
                policies=Policies(
                    max_number_acceptances=3,
                    min_acceptance_severity=Decimal("0"),
                    vulnerability_grace_period=10,
                    modified_by="integratesmanager@gmail.com",
                    min_breaking_severity=Decimal("3.9"),
                    max_acceptance_days=90,
                    modified_date=datetime.fromisoformat(
                        "2021-11-22T20:07:57+00:00"
                    ),
                    max_acceptance_severity=Decimal("3.9"),
                ),
                context="Group context test",
                disambiguation="Disambiguation test",
                description="Integrates unit test group",
                language=GroupLanguage.EN,
                created_by="integratesmanager@gmail.com",
                organization_id="38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
                name="unittesting",
                created_date=datetime.fromisoformat(
                    "2018-03-08T00:43:18+00:00"
                ),
                state=GroupState(
                    has_machine=True,
                    has_squad=True,
                    managed=GroupManaged.NOT_MANAGED,
                    modified_by="integratesmanager@gmail.com",
                    modified_date=datetime.fromisoformat(
                        "2018-03-08T00:43:18+00:00"
                    ),
                    status=GroupStateStatus.ACTIVE,
                    tier=GroupTier.MACHINE,
                    type=GroupSubscriptionType.CONTINUOUS,
                    tags=set(("test-groups", "test-updates", "test-tag")),
                    service=GroupService.WHITE,
                ),
                business_id="14441323",
                sprint_duration=2,
            ),
            [
                "can_report_vulnerabilities",
                "has_asm",
                "has_forces",
                "has_service_black",
                "has_service_white",
                "has_squad",
                "is_continuous",
                "is_fluidattacks_customer",
                "must_only_have_fluidattacks_hackers",
                "non_existing_attribute",
            ],
            [
                True,
                True,
                True,
                False,
                True,
                True,
                True,
                True,
                True,
                False,
            ],
        ],
        [
            Group(
                business_name="Testing Company and Sons",
                policies=Policies(
                    max_number_acceptances=3,
                    min_acceptance_severity=Decimal("0"),
                    vulnerability_grace_period=10,
                    modified_by="integratesmanager@gmail.com",
                    min_breaking_severity=Decimal("3.9"),
                    max_acceptance_days=90,
                    modified_date=datetime.fromisoformat(
                        "2021-11-22T20:07:57+00:00"
                    ),
                    max_acceptance_severity=Decimal("3.9"),
                ),
                context="Group context test",
                disambiguation="Disambiguation test",
                description="Oneshottest test group",
                language=GroupLanguage.EN,
                created_by="integratesmanager@gmail.com",
                organization_id="38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
                name="oneshottest",
                created_date=datetime.fromisoformat(
                    "2019-01-20T22:00:00+00:00"
                ),
                state=GroupState(
                    has_machine=True,
                    has_squad=False,
                    managed=GroupManaged.NOT_MANAGED,
                    modified_by="integratesmanager@gmail.com",
                    modified_date=datetime.fromisoformat(
                        "2019-01-20T22:00:00+00:00"
                    ),
                    status=GroupStateStatus.ACTIVE,
                    tier=GroupTier.ONESHOT,
                    type=GroupSubscriptionType.ONESHOT,
                    tags=set(("test-tag")),
                    service=GroupService.BLACK,
                ),
                business_id="14441323",
                sprint_duration=2,
            ),
            [
                "can_report_vulnerabilities",
                "has_asm",
                "has_forces",
                "has_service_black",
                "has_service_white",
                "has_squad",
                "is_continuous",
                "is_fluidattacks_customer",
                "must_only_have_fluidattacks_hackers",
                "non_existing_attribute",
            ],
            [
                True,
                True,
                False,
                True,
                False,
                False,
                False,
                True,
                True,
                False,
            ],
        ],
    ],
)
async def test_group_service_attributes_enforcer(
    group: Group,
    attributes: list,
    results: list,
) -> None:

    # All attributes must be tested for this test to succeed
    # This prevents someone to add a new attribute without testing it

    attributes_remaining_to_test: set[str] = {
        (attr)
        for attrs in authz.SERVICE_ATTRIBUTES.values()
        for attr in set(attrs).union({"non_existing_attribute"})
    }

    enforcer = authz.get_group_service_attributes_enforcer(group)

    for attribute, result in zip(attributes, results):

        assert (
            enforcer(attribute) == result
        ), f"{group.name} attribute: {attribute}, should have value {result}"

        attributes_remaining_to_test.remove(attribute)

    assert not attributes_remaining_to_test, (
        f"Please add tests for the following pairs of (group, attribute)"
        f": {attributes_remaining_to_test}"
    )
