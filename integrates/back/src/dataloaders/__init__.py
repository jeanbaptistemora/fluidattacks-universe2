from .event import (
    EventLoader,
)
from .group import (
    GroupLoader,
)
from .group_stakeholders import (
    GroupStakeholdersLoader,
)
from .organization import (
    OrganizationLoader,
)
from .organization_stakeholders import (
    OrganizationStakeholdersLoader,
)
from .organization_tags import (
    OrganizationTagsLoader,
)
from collections import (
    defaultdict,
)
from db_model.credentials.get import (
    CredentialLoader,
    GroupCredentialsLoader,
)
from db_model.findings.get import (
    FindingHistoricStateLoader,
    FindingHistoricVerificationLoader,
    FindingLoader,
    GroupDraftsAndFindingsLoader,
    GroupDraftsLoader,
    GroupFindingsLoader,
)
from db_model.roots.get import (
    GroupRootsLoader,
    RootLoader,
    RootMachineExecutionsLoader,
    RootStatesLoader,
)
from db_model.services_toe_lines.get import (
    GroupServicesToeLinesLoader,
    RootServicesToeLinesLoader,
)
from db_model.toe_inputs.get import (
    GroupToeInputsLoader,
    ToeInputLoader,
)
from db_model.toe_lines.get import (
    GroupToeLinesLoader,
    RootToeLinesLoader,
    ToeLinesLoader,
)
from db_model.vulnerabilities.get import (
    AssignedVulnerabilitiesLoader,
    FindingVulnerabilitiesLoader,
    FindingVulnerabilitiesNonDeletedLoader,
    FindingVulnerabilitiesNonZeroRiskLoader,
    FindingVulnerabilitiesOnlyZeroRiskLoader,
    RootVulnerabilitiesLoader,
    VulnerabilityHistoricStateLoader,
    VulnerabilityHistoricTreatmentLoader,
    VulnerabilityHistoricVerificationLoader,
    VulnerabilityHistoricZeroRiskLoader,
    VulnerabilityLoader,
)
from starlette.requests import (
    Request,
)
from typing import (
    NamedTuple,
    Optional,
)


class Dataloaders(NamedTuple):
    credential: CredentialLoader
    event: EventLoader
    finding: FindingLoader
    finding_historic_state: FindingHistoricStateLoader
    finding_historic_verification: FindingHistoricVerificationLoader
    finding_vulnerabilities: FindingVulnerabilitiesNonDeletedLoader
    finding_vulnerabilities_all: FindingVulnerabilitiesLoader
    finding_vulns_nzr_typed: FindingVulnerabilitiesNonZeroRiskLoader
    finding_vulns_zr_typed: FindingVulnerabilitiesOnlyZeroRiskLoader
    group: GroupLoader
    group_credentials: GroupCredentialsLoader
    group_drafts: GroupDraftsLoader
    group_drafts_and_findings: GroupDraftsAndFindingsLoader
    group_findings: GroupFindingsLoader
    group_roots: GroupRootsLoader
    group_services_toe_lines: GroupServicesToeLinesLoader
    group_stakeholders: GroupStakeholdersLoader
    group_toe_inputs: GroupToeInputsLoader
    group_toe_lines: GroupToeLinesLoader
    organization: OrganizationLoader
    organization_stakeholders: OrganizationStakeholdersLoader
    organization_tags: OrganizationTagsLoader
    me_vulnerabilities: AssignedVulnerabilitiesLoader
    root: RootLoader
    root_machine_executions: RootMachineExecutionsLoader
    root_states: RootStatesLoader
    root_services_toe_lines: RootServicesToeLinesLoader
    root_toe_lines: RootToeLinesLoader
    root_vulns: RootVulnerabilitiesLoader
    toe_input: ToeInputLoader
    toe_lines: ToeLinesLoader
    vulnerability_typed: VulnerabilityLoader
    vulnerability_historic_state: VulnerabilityHistoricStateLoader
    vulnerability_historic_treatment: VulnerabilityHistoricTreatmentLoader
    vulnerability_historic_verification: (
        VulnerabilityHistoricVerificationLoader
    )
    vulnerability_historic_zero_risk: VulnerabilityHistoricZeroRiskLoader


def apply_context_attrs(
    context: Request, loaders: Optional[Dataloaders] = None
) -> Request:
    setattr(context, "loaders", loaders if loaders else get_new_context())
    setattr(context, "store", defaultdict(lambda: None))

    return context


def get_new_context() -> Dataloaders:
    group_drafts_and_findings_loader = GroupDraftsAndFindingsLoader()
    group_findings_loader = GroupFindingsLoader(
        group_drafts_and_findings_loader
    )

    vulnerability_typed = VulnerabilityLoader()
    finding_vulnerabilities_loader = FindingVulnerabilitiesLoader(
        vulnerability_typed
    )
    finding_vulns_non_deleted_typed_loader = (
        FindingVulnerabilitiesNonDeletedLoader(finding_vulnerabilities_loader)
    )
    finding_vulns_nzr_typed_loader = FindingVulnerabilitiesNonZeroRiskLoader(
        finding_vulns_non_deleted_typed_loader
    )
    finding_vulns_zr_typed_loader = FindingVulnerabilitiesOnlyZeroRiskLoader(
        finding_vulns_non_deleted_typed_loader
    )

    return Dataloaders(
        credential=CredentialLoader(),
        event=EventLoader(),
        finding_historic_state=FindingHistoricStateLoader(),
        finding_historic_verification=(FindingHistoricVerificationLoader()),
        finding=FindingLoader(),
        finding_vulnerabilities=finding_vulns_non_deleted_typed_loader,
        finding_vulnerabilities_all=finding_vulnerabilities_loader,
        finding_vulns_nzr_typed=finding_vulns_nzr_typed_loader,
        finding_vulns_zr_typed=finding_vulns_zr_typed_loader,
        group=GroupLoader(),
        group_credentials=GroupCredentialsLoader(),
        group_drafts=GroupDraftsLoader(group_drafts_and_findings_loader),
        group_drafts_and_findings=group_drafts_and_findings_loader,
        group_findings=group_findings_loader,
        group_roots=GroupRootsLoader(),
        group_services_toe_lines=GroupServicesToeLinesLoader(),
        group_stakeholders=GroupStakeholdersLoader(),
        group_toe_inputs=GroupToeInputsLoader(),
        group_toe_lines=GroupToeLinesLoader(),
        organization=OrganizationLoader(),
        organization_stakeholders=OrganizationStakeholdersLoader(),
        organization_tags=OrganizationTagsLoader(),
        me_vulnerabilities=AssignedVulnerabilitiesLoader(),
        root=RootLoader(),
        root_services_toe_lines=RootServicesToeLinesLoader(),
        root_states=RootStatesLoader(),
        root_machine_executions=RootMachineExecutionsLoader(),
        root_toe_lines=RootToeLinesLoader(),
        root_vulns=RootVulnerabilitiesLoader(),
        toe_input=ToeInputLoader(),
        toe_lines=ToeLinesLoader(),
        vulnerability_typed=vulnerability_typed,
        vulnerability_historic_state=VulnerabilityHistoricStateLoader(),
        vulnerability_historic_treatment=(
            VulnerabilityHistoricTreatmentLoader()
        ),
        vulnerability_historic_verification=(
            VulnerabilityHistoricVerificationLoader()
        ),
        vulnerability_historic_zero_risk=VulnerabilityHistoricZeroRiskLoader(),
    )
