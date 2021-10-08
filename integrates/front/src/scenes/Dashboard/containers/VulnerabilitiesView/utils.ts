import { getLastTreatment } from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription/utils";
import type { IHistoricTreatment } from "scenes/Dashboard/containers/DescriptionView/types";
import type { IVulnDataAttr } from "scenes/Dashboard/containers/VulnerabilitiesView/HandleAcceptanceModal/types";
import type { IVulnerabilitiesAttr } from "scenes/Dashboard/containers/VulnerabilitiesView/types";

const getVulnsPendingOfAcceptation: (
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
        ? [...pendingVulns, { acceptation: "APPROVED", ...vuln }]
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
        ? [...requestedZeroRiskVulns, { acceptation: "", ...vuln }]
        : requestedZeroRiskVulns;
    },
    []
  );

function isPendingToAcceptation(
  vulnerabilities: IVulnerabilitiesAttr[]
): boolean {
  return (
    getVulnsPendingOfAcceptation(vulnerabilities).length > 0 ||
    getRequestedZeroRiskVulns(vulnerabilities).length > 0
  );
}
export {
  getVulnsPendingOfAcceptation,
  getRequestedZeroRiskVulns,
  isPendingToAcceptation,
};
