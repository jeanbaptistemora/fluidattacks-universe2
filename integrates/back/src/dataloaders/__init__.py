from .event import (
    EventLoader,
)
from .finding_vulns import (
    FindingVulnsTypedLoader,
)
from .finding_vulns_non_deleted import (
    FindingVulnsNonDeletedTypedLoader,
)
from .finding_vulns_non_zero_risk import (
    FindingVulnsNonZeroRiskTypedLoader,
)
from .finding_vulns_only_zero_risk import (
    FindingVulnsOnlyZeroRiskTypedLoader,
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
from .root_vulns import (
    RootVulnsTypedLoader,
)
from .vulnerability import (
    VulnerabilityHistoricStateLoader,
    VulnerabilityHistoricTreatmentLoader,
    VulnerabilityHistoricVerificationLoader,
    VulnerabilityHistoricZeroRiskLoader,
    VulnerabilityLoader,
    VulnerabilityTypedLoader,
)
from collections import (
    defaultdict,
)
from db_model.findings.get import (
    FindingHistoricStateLoader,
    FindingHistoricVerificationLoader,
    FindingLoader,
    GroupDraftsAndFindingsLoader,
    GroupDraftsLoader,
    GroupFindingsLoader,
    GroupRemovedFindingsLoader,
)
from db_model.roots.get import (
    GroupRootsLoader,
    RootLoader,
    RootStatesLoader,
)
from db_model.services_toe_lines.get import (
    GroupServicesToeLinesLoader,
    RootServicesToeLinesLoader,
)
from db_model.toe_inputs.get import (
    GroupToeInputsLoader,
)
from db_model.toe_lines.get import (
    GroupToeLinesLoader,
    RootToeLinesLoader,
    ToeLinesLoader,
)
from db_model.vulnerabilities.get import (
    VulnHistoricStateNewLoader,
    VulnHistoricTreatmentNewLoader,
    VulnHistoricVerificationNewLoader,
    VulnHistoricZeroRiskNewLoader,
    VulnNewLoader,
)
from starlette.requests import (
    Request,
)
from typing import (
    NamedTuple,
    Optional,
)


class Dataloaders(NamedTuple):
    event: EventLoader
    finding: FindingLoader
    finding_historic_state: FindingHistoricStateLoader
    finding_historic_verification: FindingHistoricVerificationLoader
    finding_vulns_typed: FindingVulnsNonDeletedTypedLoader  # Migration
    finding_vulns_all_typed: FindingVulnsTypedLoader  # Migration
    finding_vulns_nzr_typed: FindingVulnsNonZeroRiskTypedLoader  # Migration
    finding_vulns_zr_typed: FindingVulnsOnlyZeroRiskTypedLoader
    group: GroupLoader
    group_drafts: GroupDraftsLoader
    group_drafts_and_findings: GroupDraftsAndFindingsLoader
    group_findings: GroupFindingsLoader
    group_removed_findings: GroupRemovedFindingsLoader
    group_roots: GroupRootsLoader
    group_services_toe_lines: GroupServicesToeLinesLoader
    group_stakeholders: GroupStakeholdersLoader
    group_toe_inputs: GroupToeInputsLoader
    group_toe_lines: GroupToeLinesLoader
    organization: OrganizationLoader
    organization_stakeholders: OrganizationStakeholdersLoader
    organization_tags: OrganizationTagsLoader
    root: RootLoader
    root_states: RootStatesLoader
    root_services_toe_lines: RootServicesToeLinesLoader
    root_toe_lines: RootToeLinesLoader
    root_vulns_typed: RootVulnsTypedLoader  # Migration
    toe_lines: ToeLinesLoader
    vulnerability_typed: VulnerabilityTypedLoader
    vulnerability_historic_state: VulnerabilityHistoricStateLoader
    vulnerability_historic_treatment: VulnerabilityHistoricTreatmentLoader
    vulnerability_historic_verification: (
        VulnerabilityHistoricVerificationLoader
    )
    vulnerability_historic_zero_risk: VulnerabilityHistoricZeroRiskLoader
    vuln_historic_state_new: VulnHistoricStateNewLoader
    vuln_historic_treatment_new: VulnHistoricTreatmentNewLoader
    vuln_historic_verification_new: VulnHistoricVerificationNewLoader
    vuln_historic_zero_risk_new: VulnHistoricZeroRiskNewLoader
    vuln_new: VulnNewLoader


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

    # Migration
    finding_vulns_typed_loader = FindingVulnsTypedLoader()
    finding_vulns_non_deleted_typed_loader = FindingVulnsNonDeletedTypedLoader(
        finding_vulns_typed_loader
    )
    finding_vulns_nzr_typed_loader = FindingVulnsNonZeroRiskTypedLoader(
        finding_vulns_non_deleted_typed_loader
    )
    finding_vulns_zr_typed_loader = FindingVulnsOnlyZeroRiskTypedLoader(
        finding_vulns_typed_loader
    )

    return Dataloaders(
        event=EventLoader(),
        finding_historic_state=FindingHistoricStateLoader(),
        finding_historic_verification=(FindingHistoricVerificationLoader()),
        finding=FindingLoader(),
        finding_vulns_typed=finding_vulns_non_deleted_typed_loader,
        finding_vulns_all_typed=finding_vulns_typed_loader,
        finding_vulns_nzr_typed=finding_vulns_nzr_typed_loader,
        finding_vulns_zr_typed=finding_vulns_zr_typed_loader,
        group=GroupLoader(),
        group_drafts=GroupDraftsLoader(group_drafts_and_findings_loader),
        group_drafts_and_findings=group_drafts_and_findings_loader,
        group_findings=group_findings_loader,
        group_removed_findings=GroupRemovedFindingsLoader(),
        group_roots=GroupRootsLoader(),
        group_services_toe_lines=GroupServicesToeLinesLoader(),
        group_stakeholders=GroupStakeholdersLoader(),
        group_toe_inputs=GroupToeInputsLoader(),
        group_toe_lines=GroupToeLinesLoader(),
        organization=OrganizationLoader(),
        organization_stakeholders=OrganizationStakeholdersLoader(),
        organization_tags=OrganizationTagsLoader(),
        root=RootLoader(),
        root_services_toe_lines=RootServicesToeLinesLoader(),
        root_states=RootStatesLoader(),
        root_toe_lines=RootToeLinesLoader(),
        root_vulns_typed=RootVulnsTypedLoader(group_findings_loader),
        toe_lines=ToeLinesLoader(),
        vulnerability_typed=VulnerabilityTypedLoader(vulnerability_loader),
        vulnerability_historic_state=VulnerabilityHistoricStateLoader(
            vulnerability_loader
        ),
        vulnerability_historic_treatment=VulnerabilityHistoricTreatmentLoader(
            vulnerability_loader
        ),
        vulnerability_historic_verification=(
            VulnerabilityHistoricVerificationLoader(vulnerability_loader)
        ),
        vulnerability_historic_zero_risk=VulnerabilityHistoricZeroRiskLoader(
            vulnerability_loader
        ),
        vuln_historic_state_new=VulnHistoricStateNewLoader(),
        vuln_historic_treatment_new=VulnHistoricTreatmentNewLoader(),
        vuln_historic_verification_new=VulnHistoricVerificationNewLoader(),
        vuln_historic_zero_risk_new=VulnHistoricZeroRiskNewLoader(),
        vuln_new=VulnNewLoader(),
    )
