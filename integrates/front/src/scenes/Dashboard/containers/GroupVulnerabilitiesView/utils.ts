import type { IGroupVulnerabilities, IVulnerability } from "./types";

import type { IHistoricTreatment } from "../DescriptionView/types";
import type { IVulnerabilitiesAttr } from "../VulnerabilitiesView/types";
import type { IVulnRowAttr } from "scenes/Dashboard/components/Vulnerabilities/types";
import { formatHistoricTreatment } from "scenes/Dashboard/components/Vulnerabilities/utils";

const filterByState = (
  state: string
): ((vulnerability: IVulnerability) => boolean) => {
  return (vulnerability: IVulnerability): boolean => {
    return vulnerability.currentState === state;
  };
};

const filterByTreatment = (
  treatment: string
): ((vulnerability: IVulnerability) => boolean) => {
  return (vulnerability: IVulnerability): boolean => {
    return vulnerability.treatment === treatment;
  };
};

const formatVulnAttribute: (state: string) => string = (
  state: string
): string => {
  const vulnParameters: Record<string, string> = {
    currentState: "stateStatus",
    treatment: "treatment",
    type: "type",
    verification: "verificationStatus",
  };

  return vulnParameters[state];
};

const formatVulnerability: (data: IGroupVulnerabilities) => IVulnRowAttr[] = (
  data: IGroupVulnerabilities
): IVulnRowAttr[] => {
  const vulnerabilityFormat = data.group.vulnerabilities.edges
    .map((edge): IVulnRowAttr => edge.node)
    .map((vulnerability): IVulnRowAttr => {
      const lastTreatment: IHistoricTreatment =
        formatHistoricTreatment(vulnerability);

      return {
        ...vulnerability,
        historicTreatment: [lastTreatment],
      };
    });

  return vulnerabilityFormat;
};

const unformatTreatment: (field: string) => string = (
  field: string
): string => {
  const translationParameters: Record<string, string> = {
    "In progress": "IN_PROGRESS",
    New: "NEW",
    "Permanently accepted": "ACCEPTED_UNDEFINED",
    Rejected: "REJECTED",
    "Temporarily accepted": "ACCEPTED",
  };

  return translationParameters[field.replace(" (Pending approval)", "")];
};

function isPendingToAcceptance(
  vulnerabilitiesZeroRisk: IVulnerabilitiesAttr[]
): boolean {
  return vulnerabilitiesZeroRisk.length > 0;
}

export {
  filterByState,
  filterByTreatment,
  formatVulnAttribute,
  formatVulnerability,
  isPendingToAcceptance,
  unformatTreatment,
};
