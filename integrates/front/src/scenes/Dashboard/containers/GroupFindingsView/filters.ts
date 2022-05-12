import type { IFindingAttr } from "scenes/Dashboard/containers/GroupFindingsView/types";

function filterVerificationCount(
  findings: IFindingAttr[],
  reattack: string
): IFindingAttr[] {
  if (reattack === "Pending") {
    return findings.filter(
      (finding: IFindingAttr): boolean =>
        finding.verificationSummary.requested > 0 ||
        finding.verificationSummary.onHold > 0
    );
  } else if (reattack === "-") {
    return findings.filter(
      (finding: IFindingAttr): boolean =>
        finding.verificationSummary.requested === 0 &&
        finding.verificationSummary.onHold === 0 &&
        finding.verificationSummary.verified >= 0
    );
  }

  return findings;
}

export { filterVerificationCount };
