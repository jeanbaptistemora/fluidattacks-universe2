# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from azure_repositories.dal import (
    OrganizationRepositoriesCommitsLoader,
    OrganizationRepositoriesLoader,
)
from collections import (
    defaultdict,
)
from db_model.companies.get import (
    CompanyLoader,
)
from db_model.compliance.get import (
    ComplianceUnreliableIndicatorsLoader,
)
from db_model.credentials.get import (
    CredentialsLoader,
    OrganizationCredentialsLoader,
    UserCredentialsLoader,
)
from db_model.enrollment.get import (
    EnrollmentLoader,
)
from db_model.event_comments.get import (
    EventCommentsLoader,
)
from db_model.events.get import (
    EventLoader,
    EventsHistoricStateLoader,
    GroupEventsLoader,
)
from db_model.finding_comments.get import (
    FindingCommentsLoader,
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
from db_model.forces.get import (
    ForcesExecutionLoader,
    GroupForcesExecutionsLoader,
)
from db_model.group_access.get import (
    GroupAccessLoader,
    GroupHistoricAccessLoader,
    GroupStakeholdersAccessLoader,
    StakeholderGroupsAccessLoader,
)
from db_model.group_comments.get import (
    GroupCommentsLoader,
)
from db_model.groups.get import (
    GroupHistoricStateLoader,
    GroupLoader,
    GroupUnreliableIndicatorsLoader,
    OrganizationGroupsLoader,
)
from db_model.integration_repositories.get import (
    OrganizationUnreliableRepositoriesConnectionLoader,
    OrganizationUnreliableRepositoriesLoader,
)
from db_model.organization_access.get import (
    OrganizationAccessLoader,
    OrganizationStakeholdersAccessLoader,
    StakeholderOrganizationsAccessLoader,
)
from db_model.organizations.get import (
    OrganizationLoader,
    OrganizationUnreliableIndicatorsLoader,
)
from db_model.portfolios.get import (
    OrganizationPortfoliosLoader,
    PortfolioLoader,
)
from db_model.roots.get import (
    GitEnvironmentSecretsLoader,
    GroupRootsLoader,
    OrganizationRootsLoader,
    RootEnvironmentUrlsLoader,
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
from db_model.subscriptions.get import (
    StakeholderHistoricSubscriptionLoader,
    StakeholderSubscriptionsLoader,
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
from db_model.toe_ports.get import (
    GroupToePortsLoader,
    RootToePortsLoader,
    ToePortLoader,
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
    company: CompanyLoader
    compliance_unreliable_indicators: ComplianceUnreliableIndicatorsLoader
    credentials: CredentialsLoader
    enrollment: EnrollmentLoader
    environment_secrets: GitEnvironmentSecretsLoader
    event_historic_state: EventsHistoricStateLoader
    event: EventLoader
    event_comments: EventCommentsLoader
    event_vulnerabilities_loader: EventVulnerabilitiesLoader
    finding: FindingLoader
    finding_comments: FindingCommentsLoader
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
    forces_execution: ForcesExecutionLoader
    root_environment_urls: RootEnvironmentUrlsLoader
    group: GroupLoader
    group_access: GroupAccessLoader
    group_historic_access: GroupHistoricAccessLoader
    group_comments: GroupCommentsLoader
    group_drafts: GroupDraftsLoader
    group_drafts_and_findings: GroupDraftsAndFindingsLoader
    group_events: GroupEventsLoader
    group_findings: GroupFindingsLoader
    group_forces_executions: GroupForcesExecutionsLoader
    group_historic_state: GroupHistoricStateLoader
    group_roots: GroupRootsLoader
    group_toe_inputs: GroupToeInputsLoader
    group_toe_lines: GroupToeLinesLoader
    group_toe_ports: GroupToePortsLoader
    group_unreliable_indicators: GroupUnreliableIndicatorsLoader
    group_stakeholders_access: GroupStakeholdersAccessLoader
    me_drafts: MeDraftsLoader
    me_vulnerabilities: AssignedVulnerabilitiesLoader
    organization_access: OrganizationAccessLoader
    organization_credentials: OrganizationCredentialsLoader
    organization_groups: OrganizationGroupsLoader
    organization_integration_repositories_commits: (
        OrganizationRepositoriesCommitsLoader
    )
    organization_integration_repositories: OrganizationRepositoriesLoader
    organization_unreliable_integration_repositories: (
        OrganizationUnreliableRepositoriesLoader
    )
    organization_unreliable_integration_repositories_c: (
        OrganizationUnreliableRepositoriesConnectionLoader
    )
    organization_portfolios: OrganizationPortfoliosLoader
    organization_roots: OrganizationRootsLoader
    organization_stakeholders_access: OrganizationStakeholdersAccessLoader
    organization: OrganizationLoader
    organization_unreliable_indicators: OrganizationUnreliableIndicatorsLoader
    portfolio: PortfolioLoader
    root: RootLoader
    root_machine_executions: RootMachineExecutionsLoader
    root_historic_cloning: RootHistoricCloningLoader
    root_historic_states: RootHistoricStatesLoader
    root_secrets: RootSecretsLoader
    root_toe_inputs: RootToeInputsLoader
    root_toe_lines: RootToeLinesLoader
    root_toe_ports: RootToePortsLoader
    root_vulnerabilities: RootVulnerabilitiesLoader
    toe_input: ToeInputLoader
    toe_lines: ToeLinesLoader
    toe_port: ToePortLoader
    stakeholder: StakeholderLoader
    stakeholder_groups_access: StakeholderGroupsAccessLoader
    stakeholder_organizations_access: StakeholderOrganizationsAccessLoader
    stakeholder_subscriptions: StakeholderSubscriptionsLoader
    stakeholder_historic_subscription: StakeholderHistoricSubscriptionLoader
    stakeholder_with_fallback: StakeholderWithFallbackLoader
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


def get_new_context() -> Dataloaders:  # pylint: disable=too-many-locals
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

    event_loader = EventLoader()
    group_events_loader = GroupEventsLoader(event_loader)
    group_loader = GroupLoader()
    organization_groups_loader = OrganizationGroupsLoader(group_loader)

    stakeholder_loader = StakeholderLoader()
    stakeholder_with_fallback = StakeholderWithFallbackLoader(
        stakeholder_loader
    )
    group_access_loader = GroupAccessLoader()
    group_stakeholders_access_loader = GroupStakeholdersAccessLoader(
        group_access_loader
    )
    stakeholder_groups_access_loader = StakeholderGroupsAccessLoader(
        group_access_loader
    )
    organization_access_loader = OrganizationAccessLoader()
    organization_stakeholders_access_loader = (
        OrganizationStakeholdersAccessLoader(organization_access_loader)
    )
    stakeholder_organizations_access_loader = (
        StakeholderOrganizationsAccessLoader(organization_access_loader)
    )
    portfolio_loader = PortfolioLoader()
    organization_portfolios_loader = OrganizationPortfoliosLoader(
        portfolio_loader
    )

    return Dataloaders(
        company=CompanyLoader(),
        compliance_unreliable_indicators=(
            ComplianceUnreliableIndicatorsLoader()
        ),
        credentials=CredentialsLoader(),
        enrollment=EnrollmentLoader(),
        environment_secrets=GitEnvironmentSecretsLoader(),
        event_historic_state=EventsHistoricStateLoader(),
        event=event_loader,
        event_comments=EventCommentsLoader(),
        event_vulnerabilities_loader=EventVulnerabilitiesLoader(),
        finding_comments=FindingCommentsLoader(),
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
        forces_execution=ForcesExecutionLoader(),
        root_environment_urls=RootEnvironmentUrlsLoader(),
        group=group_loader,
        group_access=group_access_loader,
        group_historic_access=GroupHistoricAccessLoader(),
        group_comments=GroupCommentsLoader(),
        group_drafts=GroupDraftsLoader(group_drafts_and_findings_loader),
        group_drafts_and_findings=group_drafts_and_findings_loader,
        group_events=group_events_loader,
        group_findings=group_findings_loader,
        group_forces_executions=GroupForcesExecutionsLoader(),
        group_historic_state=GroupHistoricStateLoader(),
        group_roots=GroupRootsLoader(),
        group_toe_inputs=GroupToeInputsLoader(),
        group_toe_lines=GroupToeLinesLoader(),
        group_toe_ports=GroupToePortsLoader(),
        group_stakeholders_access=group_stakeholders_access_loader,
        group_unreliable_indicators=GroupUnreliableIndicatorsLoader(),
        me_drafts=MeDraftsLoader(),
        me_vulnerabilities=AssignedVulnerabilitiesLoader(),
        organization=OrganizationLoader(),
        organization_access=organization_access_loader,
        organization_groups=organization_groups_loader,
        organization_portfolios=organization_portfolios_loader,
        organization_credentials=OrganizationCredentialsLoader(),
        organization_roots=OrganizationRootsLoader(),
        organization_stakeholders_access=(
            organization_stakeholders_access_loader
        ),
        organization_unreliable_indicators=(
            OrganizationUnreliableIndicatorsLoader()
        ),
        organization_integration_repositories_commits=(
            OrganizationRepositoriesCommitsLoader()
        ),
        organization_integration_repositories=(
            OrganizationRepositoriesLoader()
        ),
        organization_unreliable_integration_repositories=(
            OrganizationUnreliableRepositoriesLoader()
        ),
        organization_unreliable_integration_repositories_c=(
            OrganizationUnreliableRepositoriesConnectionLoader()
        ),
        portfolio=portfolio_loader,
        root=RootLoader(),
        root_historic_cloning=RootHistoricCloningLoader(),
        root_historic_states=RootHistoricStatesLoader(),
        root_machine_executions=RootMachineExecutionsLoader(),
        root_secrets=RootSecretsLoader(),
        root_toe_inputs=RootToeInputsLoader(),
        root_toe_lines=RootToeLinesLoader(),
        root_toe_ports=RootToePortsLoader(),
        root_vulnerabilities=RootVulnerabilitiesLoader(),
        stakeholder=stakeholder_loader,
        stakeholder_groups_access=stakeholder_groups_access_loader,
        stakeholder_organizations_access=(
            stakeholder_organizations_access_loader
        ),
        stakeholder_subscriptions=StakeholderSubscriptionsLoader(),
        stakeholder_historic_subscription=(
            StakeholderHistoricSubscriptionLoader()
        ),
        stakeholder_with_fallback=stakeholder_with_fallback,
        toe_input=ToeInputLoader(),
        toe_lines=ToeLinesLoader(),
        toe_port=ToePortLoader(),
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
