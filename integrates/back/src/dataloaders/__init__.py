from .event import (
    EventLoader,
)
from .finding_vulns import (
    FindingVulnsLoader,
)
from .finding_vulns_non_deleted import (
    FindingVulnsNonDeletedLoader,
)
from .finding_vulns_non_zero_risk import (
    FindingVulnsNonZeroRiskLoader,
)
from .finding_vulns_only_zero_risk import (
    FindingVulnsOnlyZeroRiskLoader,
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
from .vulnerability import (
    VulnerabilityLoader,
)
from collections import (
    defaultdict,
)
from db_model.findings.get import (
    FindingHistoricStateNewLoader,
    FindingHistoricVerificationNewLoader,
    FindingNewLoader,
    GroupDraftsAndFindingsNewLoader,
    GroupDraftsNewLoader,
    GroupFindingsNewLoader,
    GroupRemovedFindingsLoader,
)
from db_model.roots.get import (
    GroupRootsLoader,
    RootLoader,
    RootStatesLoader,
)
from db_model.toe_inputs.get import (
    GroupToeInputsLoader,
)
from db_model.toe_lines.get import (
    GroupToeLinesLoader,
    RootToeLinesLoader,
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
    finding_new: FindingNewLoader
    finding_historic_state_new: FindingHistoricStateNewLoader
    finding_historic_verification_new: FindingHistoricVerificationNewLoader
    finding_vulns: FindingVulnsLoader  # All vulns except deleted
    finding_vulns_all: FindingVulnsNonDeletedLoader  # All vulns
    finding_vulns_nzr: FindingVulnsNonZeroRiskLoader
    finding_vulns_zr: FindingVulnsOnlyZeroRiskLoader
    group: GroupLoader
    group_drafts_new: GroupDraftsNewLoader
    group_findings_new: GroupFindingsNewLoader
    group_removed_findings: GroupRemovedFindingsLoader
    group_roots: GroupRootsLoader
    group_stakeholders: GroupStakeholdersLoader
    group_toe_inputs: GroupToeInputsLoader
    group_toe_lines: GroupToeLinesLoader
    organization: OrganizationLoader
    organization_stakeholders: OrganizationStakeholdersLoader
    organization_tags: OrganizationTagsLoader
    root: RootLoader
    root_states: RootStatesLoader
    root_toe_lines: RootToeLinesLoader
    vulnerability: VulnerabilityLoader
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
    group_drafts_and_findings_new_loader = GroupDraftsAndFindingsNewLoader()
    group_stakeholders_loader = GroupStakeholdersLoader()
    finding_vulns_loader = FindingVulnsLoader()
    finding_vulns_non_deleted_loader = FindingVulnsNonDeletedLoader(
        finding_vulns_loader
    )
    finding_vulns_nzr_loader = FindingVulnsNonZeroRiskLoader(
        finding_vulns_non_deleted_loader
    )
    finding_vulns_zr_loader = FindingVulnsOnlyZeroRiskLoader(
        finding_vulns_loader
    )
    root_toe_lines_loader = RootToeLinesLoader()

    return Dataloaders(
        event=EventLoader(),
        finding_historic_state_new=FindingHistoricStateNewLoader(),
        finding_historic_verification_new=(
            FindingHistoricVerificationNewLoader()
        ),
        finding_new=FindingNewLoader(),
        finding_vulns=finding_vulns_non_deleted_loader,
        finding_vulns_all=finding_vulns_loader,
        finding_vulns_nzr=finding_vulns_nzr_loader,
        finding_vulns_zr=finding_vulns_zr_loader,
        group=GroupLoader(),
        group_drafts_new=GroupDraftsNewLoader(
            group_drafts_and_findings_new_loader
        ),
        group_findings_new=GroupFindingsNewLoader(
            group_drafts_and_findings_new_loader
        ),
        group_removed_findings=GroupRemovedFindingsLoader(),
        group_roots=GroupRootsLoader(),
        group_stakeholders=group_stakeholders_loader,
        group_toe_inputs=GroupToeInputsLoader(),
        group_toe_lines=GroupToeLinesLoader(),
        organization=OrganizationLoader(),
        organization_stakeholders=OrganizationStakeholdersLoader(),
        organization_tags=OrganizationTagsLoader(),
        root=RootLoader(),
        root_states=RootStatesLoader(),
        root_toe_lines=root_toe_lines_loader,
        vulnerability=VulnerabilityLoader(),
        vuln_historic_state_new=VulnHistoricStateNewLoader(),
        vuln_historic_treatment_new=VulnHistoricTreatmentNewLoader(),
        vuln_historic_verification_new=VulnHistoricVerificationNewLoader(),
        vuln_historic_zero_risk_new=VulnHistoricZeroRiskNewLoader(),
        vuln_new=VulnNewLoader(),
    )
