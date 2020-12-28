import type { IHistoricTreatment } from "scenes/Dashboard/containers/DescriptionView/types";
import type { IVulnDataAttr } from "scenes/Dashboard/containers/VulnerabilitiesView/HandleAcceptationModal/types";
import type { IVulnerabilitiesAttr } from "scenes/Dashboard/containers/VulnerabilitiesView/types";
import { getLastTreatment } from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription/utils";

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

export { getVulnsPendingOfAcceptation, getRequestedZeroRiskVulns };
