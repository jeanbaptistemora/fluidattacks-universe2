from back.test.unit.src.utils import (  # pylint: disable=import-error
    get_module_at_test,
    set_mocks_return_values,
)
from collections.abc import (
    Iterable,
)
from custom_exceptions import (
    InvalidAcceptanceDays,
    InvalidAcceptanceSeverity,
    InvalidNumberAcceptances,
    InvalidParameter,
    InvalidPath,
    InvalidPort,
    InvalidSource,
    InvalidVulnCommitHash,
    InvalidVulnSpecific,
    InvalidVulnWhere,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
    timezone,
)
from db_model.enums import (
    Source,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityTreatmentStatus,
    VulnerabilityType,
)
from db_model.vulnerabilities.types import (
    VulnerabilityTreatment,
)
from decimal import (
    Decimal,
)
from freezegun import (
    freeze_time,
)
import pytest
from unittest.mock import (
    AsyncMock,
    patch,
)
from vulnerabilities.domain.validations import (
    validate_acceptance_days,
    validate_acceptance_severity,
    validate_number_acceptances,
    validate_path_deco,
    validate_source_deco,
    validate_updated_commit_deco,
    validate_updated_specific_deco,
    validate_updated_where_deco,
    validate_where_deco,
)

MODULE_AT_TEST = get_module_at_test(file_path=__file__)


pytestmark = [
    pytest.mark.asyncio,
]


@freeze_time("2020-10-08")
@pytest.mark.parametrize(
    ["acceptance_date", "acceptance_date_to_raise_exception", "group_name"],
    [
        [
            datetime.fromisoformat("2020-10-30 00:00:00"),
            datetime.fromisoformat("2020-10-06 23:59:59"),  # In the past
            "kurome",
        ],
        [
            datetime.fromisoformat("2020-12-07 00:00:00"),
            datetime.fromisoformat(
                "2020-12-31 00:00:00"
            ),  # Over group's max_acceptance_days
            "kurome",
        ],
    ],
)
@patch(
    MODULE_AT_TEST + "get_group_max_acceptance_days", new_callable=AsyncMock
)
@patch(MODULE_AT_TEST + "Dataloaders.group", new_callable=AsyncMock)
async def test_validate_acceptance_days(
    mock_dataloaders_group: AsyncMock,
    mock_get_group_max_acceptance_days: AsyncMock,
    acceptance_date: datetime,
    acceptance_date_to_raise_exception: datetime,
    group_name: str,
) -> None:
    mocked_objects, mocked_paths, mocks_args = [
        [
            mock_dataloaders_group.load,
            mock_get_group_max_acceptance_days,
        ],
        [
            "Dataloaders.group",
            "get_group_max_acceptance_days",
        ],
        [[group_name], [group_name]],
    ]
    assert set_mocks_return_values(
        mocks_args=mocks_args,
        mocked_objects=mocked_objects,
        module_at_test=MODULE_AT_TEST,
        paths_list=mocked_paths,
    )
    loaders: Dataloaders = get_new_context()
    await validate_acceptance_days(
        loaders, acceptance_date.astimezone(tz=timezone.utc), group_name
    )
    assert all(
        mock_object.assert_called_once for mock_object in mocked_objects
    )

    with pytest.raises(InvalidAcceptanceDays):
        await validate_acceptance_days(
            loaders,
            acceptance_date_to_raise_exception.astimezone(tz=timezone.utc),
            group_name,
        )
    assert all(mock_object.call_count == 2 for mock_object in mocked_objects)


@pytest.mark.parametrize(
    ["group_name", "severity", "severity_to_raise_exception"],
    [
        [
            "kurome",
            Decimal("6.9"),
            Decimal("8.5"),  # Over group's max_acceptance_severity
        ],
    ],
)
@patch(
    MODULE_AT_TEST + "get_group_max_acceptance_severity",
    new_callable=AsyncMock,
)
@patch(
    MODULE_AT_TEST + "get_group_min_acceptance_severity",
    new_callable=AsyncMock,
)
@patch(MODULE_AT_TEST + "Dataloaders.group", new_callable=AsyncMock)
async def test_validate_acceptance_severity(
    # pylint: disable=too-many-arguments
    mock_dataloaders_group: AsyncMock,
    mock_get_group_min_acceptance_severity: AsyncMock,
    mock_get_group_max_acceptance_severity: AsyncMock,
    group_name: str,
    severity: Decimal,
    severity_to_raise_exception: Decimal,
) -> None:
    mocked_objects, mocked_paths, mocks_args = [
        [
            mock_dataloaders_group.load,
            mock_get_group_min_acceptance_severity,
            mock_get_group_max_acceptance_severity,
        ],
        [
            "Dataloaders.group",
            "get_group_min_acceptance_severity",
            "get_group_max_acceptance_severity",
        ],
        [[group_name], [group_name], [group_name]],
    ]
    assert set_mocks_return_values(
        mocks_args=mocks_args,
        mocked_objects=mocked_objects,
        module_at_test=MODULE_AT_TEST,
        paths_list=mocked_paths,
    )
    loaders: Dataloaders = get_new_context()
    await validate_acceptance_severity(loaders, group_name, severity)
    assert all(
        mock_object.assert_called_once for mock_object in mocked_objects
    )
    with pytest.raises(InvalidAcceptanceSeverity):
        await validate_acceptance_severity(
            loaders,
            group_name,
            severity_to_raise_exception,
        )
    assert all(mock_object.call_count == 2 for mock_object in mocked_objects)


@pytest.mark.parametrize(
    [
        "group_name",
        "historic_treatment",
        "historic_treatment_to_raise_exception",
    ],
    [
        [
            "oneshottest",
            [
                VulnerabilityTreatment(
                    modified_date=datetime.fromisoformat("2020-01-01"),
                    status=VulnerabilityTreatmentStatus.ACCEPTED,
                    accepted_until=datetime.fromisoformat("2020-02-01"),
                    justification="Justification to accept the finding",
                    modified_by="unittest@fluidattacks.com",
                ),
                VulnerabilityTreatment(
                    modified_date=datetime.fromisoformat("2020-02-01"),
                    status=VulnerabilityTreatmentStatus.UNTREATED,
                ),
            ],
            [
                VulnerabilityTreatment(
                    modified_date=datetime.fromisoformat("2020-01-01"),
                    status=VulnerabilityTreatmentStatus.ACCEPTED,
                    accepted_until=datetime.fromisoformat("2020-02-01"),
                    justification="Justification to accept the finding",
                    modified_by="unittest@fluidattacks.com",
                ),
                VulnerabilityTreatment(
                    modified_date=datetime.fromisoformat("2020-01-01"),
                    status=VulnerabilityTreatmentStatus.ACCEPTED,
                    accepted_until=datetime.fromisoformat("2020-02-01"),
                    justification="Justification to accept the finding",
                    modified_by="unittest@fluidattacks.com",
                ),
                VulnerabilityTreatment(
                    modified_date=datetime.fromisoformat("2020-01-01"),
                    status=VulnerabilityTreatmentStatus.ACCEPTED,
                    accepted_until=datetime.fromisoformat("2020-02-01"),
                    justification="Justification to accept the finding",
                    modified_by="unittest@fluidattacks.com",
                ),
            ],
        ],
    ],
)
@patch(
    MODULE_AT_TEST + "get_group_max_number_acceptances", new_callable=AsyncMock
)
@patch(MODULE_AT_TEST + "Dataloaders.group", new_callable=AsyncMock)
async def test_validate_number_acceptances(
    mock_dataloaders_group: AsyncMock,
    mock_get_group_max_number_acceptances: AsyncMock,
    group_name: str,
    historic_treatment: Iterable[VulnerabilityTreatment],
    historic_treatment_to_raise_exception: Iterable[VulnerabilityTreatment],
) -> None:
    mocked_objects, mocked_paths, mocks_args = [
        [
            mock_dataloaders_group.load,
            mock_get_group_max_number_acceptances,
        ],
        [
            "Dataloaders.group",
            "get_group_max_number_acceptances",
        ],
        [[group_name], [group_name]],
    ]
    assert set_mocks_return_values(
        mocks_args=mocks_args,
        mocked_objects=mocked_objects,
        module_at_test=MODULE_AT_TEST,
        paths_list=mocked_paths,
    )
    loaders: Dataloaders = get_new_context()
    await validate_number_acceptances(loaders, group_name, historic_treatment)
    assert all(
        mock_object.assert_called_once for mock_object in mocked_objects
    )
    with pytest.raises(
        InvalidNumberAcceptances
    ) as invalida_number_acceptances:
        await validate_number_acceptances(
            loaders, group_name, historic_treatment_to_raise_exception
        )

    assert str(invalida_number_acceptances.value) == (
        "Exception - "
        "Vulnerability has been accepted the maximum number of times "
        "allowed by the defined policy"
    )
    assert all(mock_object.call_count == 2 for mock_object in mocked_objects)


def test_validate_source_deco() -> None:
    @validate_source_deco("source")
    def decorated_func(source: Source) -> Source:
        return source

    assert decorated_func(source="ANALYST")
    with pytest.raises(InvalidSource):
        decorated_func(source="USER")


def test_validate_path_deco() -> None:
    @validate_path_deco("path")
    def decorated_func(path: str) -> str:
        return path

    assert decorated_func(path="C:/Program Files/MyApp")
    with pytest.raises(InvalidPath):
        decorated_func(path="C:\\Program Files\\MyApp")


def test_validate_where_deco() -> None:
    @validate_where_deco("where")
    def decorated_func(where: str) -> str:
        return where

    assert decorated_func(where="MyVulnerability")
    with pytest.raises(InvalidVulnWhere):
        decorated_func(where="=MyVulnerability")


def test_validate_updated_specific_deco() -> None:
    @validate_updated_specific_deco("vuln_type", "specific")
    def decorated_func(vuln_type: str, specific: str) -> str:
        return vuln_type + specific

    assert decorated_func(vuln_type=VulnerabilityType.LINES, specific="210")
    assert decorated_func(vuln_type=VulnerabilityType.PORTS, specific="8080")
    with pytest.raises(InvalidVulnSpecific):
        decorated_func(vuln_type=VulnerabilityType.LINES, specific="line 200")
    with pytest.raises(InvalidPort):
        decorated_func(vuln_type=VulnerabilityType.PORTS, specific="70000")
    with pytest.raises(InvalidVulnSpecific):
        decorated_func(vuln_type=VulnerabilityType.PORTS, specific="port 80")


def test_validate_updated_commit_deco() -> None:
    @validate_updated_commit_deco("vuln_type", "commit")
    def decorated_func(vuln_type: str, commit: str) -> str:
        return vuln_type + commit

    assert decorated_func(
        vuln_type=VulnerabilityType.LINES,
        commit="da39a3ee5e6b4b0d3255bfef95601890afd80709",
    )
    with pytest.raises(InvalidParameter):
        decorated_func(
            vuln_type=VulnerabilityType.PORTS,
            commit="da39a3ee5e6b4b0d3255bfef95601890afd80709",
        )
    with pytest.raises(InvalidVulnCommitHash):
        decorated_func(
            vuln_type=VulnerabilityType.LINES,
            commit="da39a3ee5e6b4b0d3255bfey95601890afd80709",
        )
    with pytest.raises(InvalidVulnCommitHash):
        decorated_func(
            vuln_type=VulnerabilityType.LINES,
            commit="da39a3ee5e6b4b0d3255bfef95601890afd80709543",
        )


def test_validate_updated_where_deco() -> None:
    @validate_updated_where_deco("vuln_type", "where")
    def decorated_func(vuln_type: str, where: str) -> str:
        return vuln_type + where

    assert decorated_func(
        vuln_type=VulnerabilityType.LINES, where="C:/Program Files/MyApp"
    )
    with pytest.raises(InvalidPath):
        decorated_func(
            vuln_type=VulnerabilityType.LINES, where="C:\\Program Files\\MyApp"
        )
    with pytest.raises(InvalidVulnWhere):
        decorated_func(
            vuln_type=VulnerabilityType.LINES, where="=C:/Program Files/MyApp"
        )
