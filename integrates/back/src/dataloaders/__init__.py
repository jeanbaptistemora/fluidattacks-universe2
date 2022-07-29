from .stakeholder_level_role import (
    StakeholderLevelRoleLoader,
)
from collections import (
    defaultdict,
)
from dataloaders.group_access_typed import (
    GroupAccessTypedLoader,
)
from dataloaders.group_stakeholders_access import (
    GroupStakeholdersAccessLoader,
)
from dataloaders.stakeholder_groups_access import (
    StakeholderGroupsAcessLoader,
)
from db_model.credentials.get import (
    CredentialsLoader,
    OrganizationCredentialsLoader,
    UserCredentialsLoader,
)
from db_model.enrollment.get import (
    EnrollmentLoader,
)
from db_model.events.get import (
    EventLoader,
    EventsHistoricStateLoader,
    GroupEventsLoader,
)
from db_model.findings.get import (
    FindingHistoricStateLoader,
    FindingHistoricVerificationLoader,
    FindingLoader,
    GroupDraftsAndFindingsLoader,
    GroupDraftsLoader,
    GroupFindingsLoader,
    MeDraftsLoader,
)
from db_model.groups.get import (
    GroupHistoricStateLoader,
    GroupLoader,
    GroupUnreliableIndicatorsLoader,
    OrganizationGroupsLoader,
)
from db_model.organization_access.get import (
    OrganizationAccessLoader,
    OrganizationStakeholdersAccessLoader,
    StakeholderOrganizationsAccessLoader,
)
from db_model.organizations.get import (
    OrganizationLoader,
)
from db_model.portfolios.get import (
    OrganizationPortfoliosLoader,
    PortfolioLoader,
)
from db_model.roots.get import (
    GitEnvironmentSecretsLoader,
    GitEnvironmentUrlsLoader,
    GroupRootsLoader,
    OrganizationRootsLoader,
    RootHistoricCloningLoader,
    RootHistoricStatesLoader,
    RootLoader,
    RootMachineExecutionsLoader,
    RootSecretsLoader,
)
from db_model.stakeholders.get import (
    StakeholderLoader,
    StakeholderWithFallbackLoader,
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
    credentials: CredentialsLoader
    enrollment: EnrollmentLoader
    environment_secrets: GitEnvironmentSecretsLoader
    event_historic_state: EventsHistoricStateLoader
    event: EventLoader
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
    git_environment_urls: GitEnvironmentUrlsLoader
    group: GroupLoader
    group_access: GroupAccessTypedLoader
    group_drafts: GroupDraftsLoader
    group_drafts_and_findings: GroupDraftsAndFindingsLoader
    group_events: GroupEventsLoader
    group_findings: GroupFindingsLoader
    group_historic_state: GroupHistoricStateLoader
    group_roots: GroupRootsLoader
    group_toe_inputs: GroupToeInputsLoader
    group_toe_lines: GroupToeLinesLoader
    group_unreliable_indicators: GroupUnreliableIndicatorsLoader
    group_stakeholders_access: GroupStakeholdersAccessLoader
    stakeholder_groups_access: StakeholderGroupsAcessLoader
    me_vulnerabilities: AssignedVulnerabilitiesLoader
    organization_access: OrganizationAccessLoader
    organization_credentials: OrganizationCredentialsLoader
    me_drafts: MeDraftsLoader
    organization_groups: OrganizationGroupsLoader
    organization_portfolios: OrganizationPortfoliosLoader
    organization_roots: OrganizationRootsLoader
    organization_stakeholders_access: OrganizationStakeholdersAccessLoader
    organization: OrganizationLoader
    portfolio: PortfolioLoader
    root: RootLoader
    root_machine_executions: RootMachineExecutionsLoader
    root_secrets: RootSecretsLoader
    root_historic_cloning: RootHistoricCloningLoader
    root_historic_states: RootHistoricStatesLoader
    root_toe_inputs: RootToeInputsLoader
    root_toe_lines: RootToeLinesLoader
    root_vulnerabilities: RootVulnerabilitiesLoader
    toe_input: ToeInputLoader
    toe_lines: ToeLinesLoader
    stakeholder: StakeholderLoader
    stakeholder_with_fallback: StakeholderWithFallbackLoader
    stakeholder_level_role: StakeholderLevelRoleLoader
    stakeholder_organizations_access: StakeholderOrganizationsAccessLoader
    user_credentials: UserCredentialsLoader
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

    vulnerability_loader = VulnerabilityLoader()
    finding_vulnerabilities_loader = FindingVulnerabilitiesLoader(
        vulnerability_loader
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

    stakeholder_loader = StakeholderLoader()
    stakeholder_with_fallback = StakeholderWithFallbackLoader(
        stakeholder_loader
    )

    return Dataloaders(
        credentials=CredentialsLoader(),
        enrollment=EnrollmentLoader(),
        environment_secrets=GitEnvironmentSecretsLoader(),
        event_historic_state=EventsHistoricStateLoader(),
        event=EventLoader(),
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
        git_environment_urls=GitEnvironmentUrlsLoader(),
        group=GroupLoader(),
        group_access=GroupAccessTypedLoader(),
        group_drafts=GroupDraftsLoader(group_drafts_and_findings_loader),
        group_drafts_and_findings=group_drafts_and_findings_loader,
        group_events=GroupEventsLoader(),
        group_findings=group_findings_loader,
        group_historic_state=GroupHistoricStateLoader(),
        group_roots=GroupRootsLoader(),
        group_toe_inputs=GroupToeInputsLoader(),
        group_toe_lines=GroupToeLinesLoader(),
        group_unreliable_indicators=GroupUnreliableIndicatorsLoader(),
        group_stakeholders_access=GroupStakeholdersAccessLoader(),
        stakeholder_groups_access=StakeholderGroupsAcessLoader(),
        me_vulnerabilities=AssignedVulnerabilitiesLoader(),
        me_drafts=MeDraftsLoader(),
        organization_access=OrganizationAccessLoader(),
        organization_groups=OrganizationGroupsLoader(),
        organization_portfolios=OrganizationPortfoliosLoader(),
        organization_credentials=OrganizationCredentialsLoader(),
        organization_roots=OrganizationRootsLoader(),
        organization_stakeholders_access=(
            OrganizationStakeholdersAccessLoader()
        ),
        organization=OrganizationLoader(),
        portfolio=PortfolioLoader(),
        root=RootLoader(),
        root_machine_executions=RootMachineExecutionsLoader(),
        root_historic_cloning=RootHistoricCloningLoader(),
        root_historic_states=RootHistoricStatesLoader(),
        root_secrets=RootSecretsLoader(),
        root_toe_inputs=RootToeInputsLoader(),
        root_toe_lines=RootToeLinesLoader(),
        root_vulnerabilities=RootVulnerabilitiesLoader(),
        stakeholder=stakeholder_loader,
        stakeholder_with_fallback=stakeholder_with_fallback,
        stakeholder_level_role=StakeholderLevelRoleLoader(),
        stakeholder_organizations_access=(
            StakeholderOrganizationsAccessLoader()
        ),
        toe_input=ToeInputLoader(),
        toe_lines=ToeLinesLoader(),
        user_credentials=UserCredentialsLoader(),
        vulnerability=vulnerability_loader,
        vulnerability_historic_state=VulnerabilityHistoricStateLoader(),
        vulnerability_historic_treatment=(
            VulnerabilityHistoricTreatmentLoader()
        ),
        vulnerability_historic_verification=(
            VulnerabilityHistoricVerificationLoader()
        ),
        vulnerability_historic_zero_risk=VulnerabilityHistoricZeroRiskLoader(),
    )
