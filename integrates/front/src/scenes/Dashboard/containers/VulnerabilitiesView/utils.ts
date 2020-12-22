import type { IHistoricTreatment } from "scenes/Dashboard/containers/DescriptionView/types";
import type { IVulnDataAttr } from "scenes/Dashboard/containers/VulnerabilitiesView/HandleAcceptationModal/types";
import type { IVulnerabilities } from "scenes/Dashboard/containers/VulnerabilitiesView/types";
import { getLastTreatment } from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription/utils";

const getVulnsPendingOfAcceptation: (
  vulnerabilities: IVulnerabilities[]
) => IVulnDataAttr[] = (vulnerabilities: IVulnerabilities[]): IVulnDataAttr[] =>
  vulnerabilities.reduce(
    (
      pendingVulns: IVulnDataAttr[],
      vuln: IVulnerabilities
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
  vulnerabilities: IVulnerabilities[]
) => IVulnDataAttr[] = (vulnerabilities: IVulnerabilities[]): IVulnDataAttr[] =>
  vulnerabilities.reduce(
    (
      requestedZeroRiskVulns: IVulnDataAttr[],
      vuln: IVulnerabilities
    ): IVulnDataAttr[] => {
      return vuln.zeroRisk === "Requested"
        ? [...requestedZeroRiskVulns, { acceptation: "", ...vuln }]
        : requestedZeroRiskVulns;
    },
    []
  );

export { getVulnsPendingOfAcceptation, getRequestedZeroRiskVulns };
