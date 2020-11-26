import type { IHistoricTreatment } from "scenes/Dashboard/containers/DescriptionView/types";
import type { IVulnData } from "scenes/Dashboard/containers/VulnerabilitiesView/HandleAcceptationModal/types";
import type { IVulnerabilities } from "scenes/Dashboard/containers/VulnerabilitiesView/types";
import { getLastTreatment } from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription/utils";

const getVulnsPendingOfAcceptation: (
  vulnerabilities: IVulnerabilities[]
) => IVulnData[] = (vulnerabilities: IVulnerabilities[]): IVulnData[] =>
  vulnerabilities.reduce(
    (pendingVulns: IVulnData[], vuln: IVulnerabilities): IVulnData[] => {
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

export { getVulnsPendingOfAcceptation };
