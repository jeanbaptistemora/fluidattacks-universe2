# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# pylint: disable=import-error
from back.test.unit.src.utils import (
    create_dummy_info,
    create_dummy_session,
)
from custom_exceptions import (
    CouldNotVerifyStakeholder,
    ErrorUploadingFileS3,
    EventNotFound,
    FindingNamePolicyNotFound,
    GroupNotFound,
    InvalidAcceptanceDays,
    InvalidAcceptanceSeverity,
    InvalidFileType,
    InvalidGroupServicesConfig,
    InvalidNumberAcceptances,
    InvalidPushToken,
    InvalidRange,
    InvalidSchema,
    OrganizationNotFound,
    RepeatedValues,
    StakeholderNotFound,
    UnableToSendSms,
    UnavailabilityError,
    VulnNotFound,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
    timedelta,
)
from db_model.groups.enums import (
    GroupService,
    GroupStateUpdationJustification,
    GroupSubscriptionType,
    GroupTier,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityTreatmentStatus,
)
from db_model.vulnerabilities.types import (
    VulnerabilityTreatment,
)
from findings.domain import (
    validate_evidence,
)
from freezegun import (
    freeze_time,
)
from groups.domain import (
    send_mail_devsecops_agent,
    update_group,
    validate_group_services_config,
    validate_group_tags,
)
from newutils.vulnerabilities import (
    range_to_list,
)
from organizations_finding_policies import (
    domain as policies_domain,
)
import os
import pytest
from s3 import (
    operations as s3_ops,
)
from sms.common import (
    send_sms_notification,
)
from stakeholders import (
    domain as stakeholders_domain,
)
from starlette.datastructures import (
    UploadFile,
)
from twilio.base.exceptions import (
    TwilioRestException,
)
from unittest import (
    mock,
)
import uuid
from verify.operations import (
    check_verification,
)
from vulnerabilities.domain import (
    send_treatment_report_mail,
    validate_treatment_change,
)
from vulnerability_files.domain import (
    validate_file_schema,
)
import yaml

pytestmark = [
    pytest.mark.asyncio,
]


async def test_exception_could_not_verify_stake_holder() -> None:
    test_code = "US"
    with pytest.raises(CouldNotVerifyStakeholder):
        with mock.patch("verify.operations.FI_ENVIRONMENT", "production"):
            await check_verification(phone_number="", code=test_code)


async def test_exception_error_uploading_file_s3() -> None:
    bucket_name = "test_bucket"
    file_name = "test-anim.gif"
    file_location = os.path.dirname(os.path.abspath(__file__))
    file_location = os.path.join(file_location, "mock/" + file_name)
    with pytest.raises(ErrorUploadingFileS3):
        with open(file_location, "rb") as data:
            await s3_ops.upload_memory_file(
                bucket_name,
                data,
                file_name,
            )


async def test_exception_event_not_found() -> None:
    loaders: Dataloaders = get_new_context()
    with pytest.raises(EventNotFound):
        await loaders.event.load("000001111")


async def test_exception_finding_name_policy_not_found() -> None:
    org_name = "okada"
    with pytest.raises(FindingNamePolicyNotFound):
        assert await policies_domain.get_finding_policy(
            org_name=org_name,
            finding_policy_id="5d92c7eb-816f-43d5-9361-c0672837e7ab",
        )


@pytest.mark.changes_db
@pytest.mark.parametrize(
    [
        "group_name",
        "responsible",
        "had_token",
    ],
    [
        [
            "not-exist",
            "integratesmanager@gmail.com",
            True,
        ],
        [
            "not-exist",
            "integratesmanager@gmail.com",
            False,
        ],
    ],
)
async def test_send_mail_devsecops_agent_fail(
    group_name: str,
    responsible: str,
    had_token: bool,
) -> None:
    with pytest.raises(GroupNotFound):
        await send_mail_devsecops_agent(
            loaders=get_new_context(),
            group_name=group_name,
            responsible=responsible,
            had_token=had_token,
        )


@pytest.mark.changes_db
@pytest.mark.parametrize(
    [
        "group_name",
        "service",
        "subscription",
        "has_machine",
        "has_squad",
        "has_arm",
        "tier",
    ],
    [
        [
            "not-exists",
            GroupService.WHITE,
            GroupSubscriptionType.CONTINUOUS,
            True,
            True,
            True,
            GroupTier.MACHINE,
        ],
        [
            "not-exists",
            GroupService.WHITE,
            GroupSubscriptionType.CONTINUOUS,
            False,
            False,
            False,
            GroupTier.FREE,
        ],
    ],  # pylint: disable=too-many-arguments
)
async def test_update_group_attrs_fail(
    group_name: str,
    service: GroupService,
    subscription: GroupSubscriptionType,
    has_machine: bool,
    has_squad: bool,
    has_arm: bool,
    tier: GroupTier,
) -> None:
    with pytest.raises(GroupNotFound):
        await update_group(
            loaders=get_new_context(),
            comments="",
            email="test@test.test",
            group_name=group_name,
            justification=GroupStateUpdationJustification.NONE,
            has_arm=has_arm,
            has_machine=has_machine,
            has_squad=has_squad,
            service=service,
            subscription=subscription,
            tier=tier,
        )


@freeze_time("2020-10-08")
@pytest.mark.parametrize(
    ["acceptance_date"],
    [
        ["2020-10-06 23:59:59"],  # In the past
        ["2020-12-31 00:00:00"],  # Over org's max_acceptance_days
    ],
)
async def test_validate_past_acceptance_days(acceptance_date: str) -> None:
    historic_treatment = (
        VulnerabilityTreatment(
            modified_date="2020-02-01T17:00:00+00:00",
            status=VulnerabilityTreatmentStatus.NEW,
        ),
    )
    severity = 5
    values_accepted = {
        "justification": "This is a test treatment justification",
        "bts_url": "",
        "treatment": "ACCEPTED",
        "acceptance_date": acceptance_date,
    }
    with pytest.raises(InvalidAcceptanceDays):
        await validate_treatment_change(
            finding_severity=severity,
            group_name="kurome",
            historic_treatment=historic_treatment,
            loaders=get_new_context(),
            values=values_accepted,
        )


async def test_validate_acceptance_severity() -> None:
    historic_treatment = (
        VulnerabilityTreatment(
            modified_date="2020-02-01T17:00:00+00:00",
            status=VulnerabilityTreatmentStatus.NEW,
        ),
    )
    severity = 8.5
    acceptance_date = (datetime.now() + timedelta(days=10)).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    values_accepted = {
        "justification": "This is a test treatment justification",
        "bts_url": "",
        "treatment": "ACCEPTED",
        "acceptance_date": acceptance_date,
    }
    with pytest.raises(InvalidAcceptanceSeverity):
        await validate_treatment_change(
            finding_severity=severity,
            group_name="kurome",
            historic_treatment=historic_treatment,
            loaders=get_new_context(),
            values=values_accepted,
        )


async def test_validate_evidence_records_invalid_type() -> None:
    evidence_id = "fileRecords"
    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(filename, "mock/test-anim.gif")
    mime_type = "image/gif"
    with open(filename, "rb") as test_file:
        uploaded_file = UploadFile(
            "test-file-records.csv", test_file, mime_type
        )
        with pytest.raises(InvalidFileType):
            await validate_evidence(evidence_id, uploaded_file)


async def test_validate_group_services_config() -> None:
    with pytest.raises(InvalidGroupServicesConfig):
        validate_group_services_config(True, True, False)
    with pytest.raises(InvalidGroupServicesConfig):
        validate_group_services_config(False, True, True)


async def test_validate_number_acceptances() -> None:
    historic_treatment = (
        VulnerabilityTreatment(
            modified_date="2020-01-01T17:00:00+00:00",
            status=VulnerabilityTreatmentStatus.ACCEPTED,
            accepted_until="2020-02-01T17:00:00+00:00",
            justification="Justification to accept the finding",
            modified_by="unittest@fluidattacks.com",
        ),
        VulnerabilityTreatment(
            modified_date="2020-02-01T17:00:00+00:00",
            status=VulnerabilityTreatmentStatus.NEW,
        ),
    )
    severity = 5
    acceptance_date = (datetime.now() + timedelta(days=10)).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    values_accepted = {
        "justification": "This is a test treatment justification",
        "bts_url": "",
        "treatment": "ACCEPTED",
        "acceptance_date": acceptance_date,
    }
    with pytest.raises(InvalidNumberAcceptances):
        await validate_treatment_change(
            finding_severity=severity,
            group_name="kurome",
            historic_treatment=historic_treatment,
            loaders=get_new_context(),
            values=values_accepted,
        )


async def test_add_push_token() -> None:
    loaders: Dataloaders = get_new_context()
    user_email = "unittest@fluidattacks.com"
    with pytest.raises(InvalidPushToken):
        assert await stakeholders_domain.add_push_token(  # type: ignore
            loaders, user_email, "not-a-push-token"
        )


def test_invalid_range_to_list() -> None:
    bad_range_value = "13-12"
    with pytest.raises(InvalidRange):
        assert range_to_list(bad_range_value)


async def test_validate_file_schema_invalid() -> None:
    finding_id = "463461507"
    request = await create_dummy_session("unittest@fluidattacks.com")
    info = create_dummy_info(request)
    # FP: the generated filename is unpredictable
    file_url = (  # NOSONAR
        f"/tmp/vulnerabilities-{uuid.uuid4()}-{finding_id}.yaml"
    )
    with open(file_url, "w", encoding="utf-8") as stream:
        yaml.safe_dump("", stream)
    with pytest.raises(InvalidSchema):  # NOQA
        await validate_file_schema(file_url, info)  # type: ignore


async def test_organization_not_found() -> None:
    with pytest.raises(OrganizationNotFound):
        loaders: Dataloaders = get_new_context()
        await loaders.organization.load("madeup-org")
    with pytest.raises(OrganizationNotFound):
        new_loader: Dataloaders = get_new_context()
        await new_loader.organization.load("ORG#madeup-id")


async def test_validate_tags() -> None:
    loaders: Dataloaders = get_new_context()
    with pytest.raises(RepeatedValues):
        assert await validate_group_tags(
            loaders, "unittesting", ["same-name", "same-name", "another-one"]
        )
    with pytest.raises(RepeatedValues):
        assert await validate_group_tags(
            loaders, "unittesting", ["test-groups"]
        )


@pytest.mark.changes_db
async def test_remove_stakeholder() -> None:
    email: str = "testanewuser@test.test"
    loaders: Dataloaders = get_new_context()
    with pytest.raises(StakeholderNotFound):
        await loaders.stakeholder.load(email)


async def test_exception_unable_to_send_sms() -> None:
    status = 500
    uri = "/Accounts/ACXXXXXXXXXXXXXXXXX/Messages.json"
    test_phone_number = "12345678"
    test_message = "This is a test message"
    with mock.patch("sms.common.FI_ENVIRONMENT", "production"):
        with mock.patch("sms.common.client.messages.create") as mock_twilio:
            mock_twilio.side_effect = TwilioRestException(status, uri)
            with pytest.raises(UnableToSendSms):
                await send_sms_notification(
                    phone_number=test_phone_number,
                    message_body=test_message,
                )


async def test_exception_unavailability_error() -> None:
    bucket_name = "bad_test_bucket"
    file_name = "test-anim.gif"
    file_location = os.path.dirname(os.path.abspath(__file__))
    file_location = os.path.join(file_location, "mock/" + file_name)
    with pytest.raises(UnavailabilityError):
        with open(file_location, "rb"):
            test_file = UploadFile(filename=file_name)
            await s3_ops.upload_memory_file(
                bucket_name,
                test_file,
                file_name,
            )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    [
        "modified_by",
        "justification",
        "vulnerability_id",
        "is_approved",
    ],
    [
        [
            "vulnmanager@gmail.com",
            "test",
            "be09edb7-cd5c-47ed-bee4-97c645acdce9",
            False,
        ],
    ],
)
async def test_send_treatment_report_mail_fail(
    modified_by: str,
    justification: str,
    vulnerability_id: str,
    is_approved: bool,
) -> None:
    with pytest.raises(VulnNotFound):
        await send_treatment_report_mail(
            loaders=get_new_context(),
            modified_by=modified_by,
            justification=justification,
            vulnerability_id=vulnerability_id,
            is_approved=is_approved,
        )
