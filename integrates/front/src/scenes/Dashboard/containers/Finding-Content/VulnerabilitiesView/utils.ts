import { getLastTreatment } from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription/utils";
import type { IHistoricTreatment } from "scenes/Dashboard/containers/Finding-Content/DescriptionView/types";
import type { IVulnDataAttr } from "scenes/Dashboard/containers/Finding-Content/VulnerabilitiesView/HandleAcceptanceModal/types";
import type { IVulnerabilitiesAttr } from "scenes/Dashboard/containers/Finding-Content/VulnerabilitiesView/types";

const getVulnsPendingOfAcceptance: (
  vulnerabilities: IVulnerabilitiesAttr[]
) => IVulnDataAttr[] = (
  vulnerabilities: IVulnerabilitiesAttr[]
): IVulnDataAttr[] =>
  vulnerabilities.reduce(
    (
      pendingVulns: IVulnDataAttr[],
      vuln: IVulnerabilitiesAttr
    ): IVulnDataAttr[] => {
      const lastTreatment: IHistoricTreatment = getLastTreatment(
        vuln.historicTreatment
      );

      return lastTreatment.treatment === "ACCEPTED_UNDEFINED" &&
        lastTreatment.acceptanceStatus === "SUBMITTED"
        ? [...pendingVulns, { acceptance: "APPROVED", ...vuln }]
        : pendingVulns;
    },
    []
  );

const getRequestedZeroRiskVulns: (
  vulnerabilities: IVulnerabilitiesAttr[]
) => IVulnDataAttr[] = (
  vulnerabilities: IVulnerabilitiesAttr[]
): IVulnDataAttr[] =>
  vulnerabilities.reduce(
    (
      requestedZeroRiskVulns: IVulnDataAttr[],
      vuln: IVulnerabilitiesAttr
    ): IVulnDataAttr[] => {
      return vuln.zeroRisk === "Requested"
        ? [...requestedZeroRiskVulns, { acceptance: "", ...vuln }]
        : requestedZeroRiskVulns;
    },
    []
  );

const getSubmittedVulns: (
  vulnerabilities: IVulnerabilitiesAttr[]
) => IVulnDataAttr[] = (
  vulnerabilities: IVulnerabilitiesAttr[]
): IVulnDataAttr[] =>
  vulnerabilities.reduce(
    (
      submittedVulns: IVulnDataAttr[],
      vuln: IVulnerabilitiesAttr
    ): IVulnDataAttr[] => {
      return vuln.state === "SUBMITTED"
        ? [...submittedVulns, { acceptance: "", ...vuln }]
        : submittedVulns;
    },
    []
  );

function isPendingToAcceptance(
  vulnerabilities: IVulnerabilitiesAttr[]
): boolean {
  return (
    getVulnsPendingOfAcceptance(vulnerabilities).length > 0 ||
    getRequestedZeroRiskVulns(vulnerabilities).length > 0
  );
}
export {
  getVulnsPendingOfAcceptance,
  getRequestedZeroRiskVulns,
  getSubmittedVulns,
  isPendingToAcceptance,
};
