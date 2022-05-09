from .event import (
    EventLoader,
    EventTypedLoader,
)
from .group import (
    GroupHistoricStateTypedLoader,
    GroupIndicatorsTypedLoader,
    GroupTypedLoader,
    OrganizationGroupsTypedLoader,
)
from .group_stakeholders import (
    GroupStakeholdersLoader,
)
from .organization import (
    OrganizationLoader,
    OrganizationTypedLoader,
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
    GitEnvironmentSecretsLoader,
    GitEnvironmentUrlsLoader,
    GroupRootsLoader,
    OrganizationRootsLoader,
    RootLoader,
    RootMachineExecutionsLoader,
    RootSecretsLoader,
    RootStatesLoader,
)
from db_model.toe_inputs.get import (
    GroupToeInputsLoader,
    RootToeInputsLoader,
    ToeInputLoader,
)
from db_model.toe_lines.get import (
    GroupToeLinesLoader,
    RootToeLinesLoader,
    ToeLinesLoader,
)
from db_model.users.get import (
    UserLoader,
)
from db_model.vulnerabilities.get import (
    AssignedVulnerabilitiesLoader,
    EventVulnerabilitiesLoader,
    FindingVulnerabilitiesLoader,
    FindingVulnerabilitiesNonDeletedLoader,
    FindingVulnerabilitiesNonZeroRiskConnectionLoader,
    FindingVulnerabilitiesNonZeroRiskLoader,
    FindingVulnerabilitiesOnlyZeroRiskConnectionLoader,
    FindingVulnerabilitiesOnlyZeroRiskLoader,
    FindingVulnerabilitiesToReattackConnectionLoader,
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
    event_typed: EventTypedLoader
    event_vulnerabilities_loader: EventVulnerabilitiesLoader
    finding: FindingLoader
    finding_historic_state: FindingHistoricStateLoader
    finding_historic_verification: FindingHistoricVerificationLoader
    finding_vulnerabilities: FindingVulnerabilitiesNonDeletedLoader
    finding_vulnerabilities_all: FindingVulnerabilitiesLoader
    finding_vulnerabilities_nzr: FindingVulnerabilitiesNonZeroRiskLoader
    finding_vulnerabilities_nzr_c: (
        FindingVulnerabilitiesNonZeroRiskConnectionLoader
    )
    finding_vulnerabilities_to_reattack_c: (
        FindingVulnerabilitiesToReattackConnectionLoader
    )
    finding_vulnerabilities_zr: FindingVulnerabilitiesOnlyZeroRiskLoader
    finding_vulnerabilities_zr_c: (
        FindingVulnerabilitiesOnlyZeroRiskConnectionLoader
    )
    me_vulnerabilities: AssignedVulnerabilitiesLoader
    group_credentials: GroupCredentialsLoader
    group_drafts: GroupDraftsLoader
    group_drafts_and_findings: GroupDraftsAndFindingsLoader
    group_findings: GroupFindingsLoader
    group_historic_state_typed: GroupHistoricStateTypedLoader
    group_indicators_typed: GroupIndicatorsTypedLoader
    group_roots: GroupRootsLoader
    group_stakeholders: GroupStakeholdersLoader
    group_toe_inputs: GroupToeInputsLoader
    group_toe_lines: GroupToeLinesLoader
    group_typed: GroupTypedLoader
    organization: OrganizationLoader
    organization_groups_typed: OrganizationGroupsTypedLoader
    organization_roots: OrganizationRootsLoader
    organization_stakeholders: OrganizationStakeholdersLoader
    organization_typed: OrganizationTypedLoader
    organization_tags: OrganizationTagsLoader
    root: RootLoader
    root_machine_executions: RootMachineExecutionsLoader
    root_secrets: RootSecretsLoader
    environment_secrets: GitEnvironmentSecretsLoader
    git_environment_urls: GitEnvironmentUrlsLoader
    root_states: RootStatesLoader
    root_toe_inputs: RootToeInputsLoader
    root_toe_lines: RootToeLinesLoader
    root_vulnerabilities: RootVulnerabilitiesLoader
    toe_input: ToeInputLoader
    toe_lines: ToeLinesLoader
    user: UserLoader
    vulnerability: VulnerabilityLoader
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

    vulnerability = VulnerabilityLoader()
    finding_vulnerabilities_loader = FindingVulnerabilitiesLoader(
        vulnerability
    )
    finding_vulns_non_deleted_loader = FindingVulnerabilitiesNonDeletedLoader(
        finding_vulnerabilities_loader
    )
    finding_vulnerabilities_nzr_loader = (
        FindingVulnerabilitiesNonZeroRiskLoader(
            finding_vulns_non_deleted_loader
        )
    )
    finding_vulnerabilities_zr_loader = (
        FindingVulnerabilitiesOnlyZeroRiskLoader(
            finding_vulns_non_deleted_loader
        )
    )

    return Dataloaders(
        credential=CredentialLoader(),
        event=EventLoader(),
        event_typed=EventTypedLoader(),
        event_vulnerabilities_loader=EventVulnerabilitiesLoader(),
        finding_historic_state=FindingHistoricStateLoader(),
        finding_historic_verification=(FindingHistoricVerificationLoader()),
        finding=FindingLoader(),
        finding_vulnerabilities=finding_vulns_non_deleted_loader,
        finding_vulnerabilities_all=finding_vulnerabilities_loader,
        finding_vulnerabilities_nzr=finding_vulnerabilities_nzr_loader,
        finding_vulnerabilities_nzr_c=(
            FindingVulnerabilitiesNonZeroRiskConnectionLoader()
        ),
        finding_vulnerabilities_to_reattack_c=(
            FindingVulnerabilitiesToReattackConnectionLoader()
        ),
        finding_vulnerabilities_zr=finding_vulnerabilities_zr_loader,
        finding_vulnerabilities_zr_c=(
            FindingVulnerabilitiesOnlyZeroRiskConnectionLoader()
        ),
        me_vulnerabilities=AssignedVulnerabilitiesLoader(),
        group_credentials=GroupCredentialsLoader(),
        group_drafts=GroupDraftsLoader(group_drafts_and_findings_loader),
        group_drafts_and_findings=group_drafts_and_findings_loader,
        group_findings=group_findings_loader,
        group_historic_state_typed=GroupHistoricStateTypedLoader(),
        group_indicators_typed=GroupIndicatorsTypedLoader(),
        group_roots=GroupRootsLoader(),
        group_stakeholders=GroupStakeholdersLoader(),
        group_toe_inputs=GroupToeInputsLoader(),
        group_toe_lines=GroupToeLinesLoader(),
        group_typed=GroupTypedLoader(),
        organization=OrganizationLoader(),
        organization_groups_typed=OrganizationGroupsTypedLoader(),
        organization_roots=OrganizationRootsLoader(),
        organization_stakeholders=OrganizationStakeholdersLoader(),
        organization_tags=OrganizationTagsLoader(),
        organization_typed=OrganizationTypedLoader(),
        root=RootLoader(),
        root_machine_executions=RootMachineExecutionsLoader(),
        root_states=RootStatesLoader(),
        root_secrets=RootSecretsLoader(),
        environment_secrets=GitEnvironmentSecretsLoader(),
        git_environment_urls=GitEnvironmentUrlsLoader(),
        root_toe_inputs=RootToeInputsLoader(),
        root_toe_lines=RootToeLinesLoader(),
        root_vulnerabilities=RootVulnerabilitiesLoader(),
        toe_input=ToeInputLoader(),
        toe_lines=ToeLinesLoader(),
        user=UserLoader(),
        vulnerability=vulnerability,
        vulnerability_historic_state=VulnerabilityHistoricStateLoader(),
        vulnerability_historic_treatment=(
            VulnerabilityHistoricTreatmentLoader()
        ),
        vulnerability_historic_verification=(
            VulnerabilityHistoricVerificationLoader()
        ),
        vulnerability_historic_zero_risk=VulnerabilityHistoricZeroRiskLoader(),
    )
