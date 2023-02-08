from db_model.findings.types import (
    Finding,
)
from db_model.groups.types import (
    Group,
)
from db_model.organizations.types import (
    Organization,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
from typing import (
    Any,
    NamedTuple,
)


class AddOrganizationPayload(NamedTuple):
    success: bool
    organization: Organization


class GrantStakeholderAccessPayload(NamedTuple):
    success: bool
    granted_stakeholder: Stakeholder


class AddConsultPayload(NamedTuple):
    success: bool
    comment_id: str


class AddStakeholderPayload(NamedTuple):
    success: bool
    email: str


class AddDraftPayload(NamedTuple):
    draft_id: str
    success: bool


class AddRootPayload(NamedTuple):
    root_id: str
    success: bool


class AddEventPayload(NamedTuple):
    event_id: str
    success: bool


class ApproveDraftPayload(NamedTuple):
    success: bool
    release_date: str


class DownloadFilePayload(NamedTuple):
    success: bool
    url: str


class UpdateStakeholderPayload(NamedTuple):
    success: bool
    modified_stakeholder: dict[str, Any]


class UpdateToeInputPayload(NamedTuple):
    component: str
    entry_point: str
    group_name: str
    root_id: str
    success: bool


class UpdateToeLinesPayload(NamedTuple):
    filename: str
    group_name: str
    root_id: str
    success: bool


class UpdateToePortPayload(NamedTuple):
    address: str
    port: str
    group_name: str
    root_id: str
    success: bool


class ExecuteMachinePayload(NamedTuple):
    success: bool
    pipeline_url: str


class RemoveStakeholderAccessPayload(NamedTuple):
    success: bool
    removed_email: str


class SimpleFindingPayload(NamedTuple):
    success: bool
    finding: Finding


class SimpleGroupPayload(NamedTuple):
    success: bool
    group: Group


class SimplePayload(NamedTuple):
    success: bool


class SimplePayloadMessage(NamedTuple):
    success: bool
    message: str


class UpdateAccessTokenPayload(NamedTuple):
    success: bool
    session_jwt: str


class SignPostUrlsPayload(NamedTuple):
    success: bool
    url: dict[str, Any]
