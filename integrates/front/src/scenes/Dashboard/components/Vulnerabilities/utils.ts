import type { IHistoricTreatment } from "scenes/Dashboard/containers/DescriptionView/types";
import type { IVulnRowAttr } from "scenes/Dashboard/components/Vulnerabilities/types";
import _ from "lodash";
import { formatDropdownField } from "utils/formatHelpers";
import { getLastTreatment } from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription/utils";
import { translate } from "utils/translations/translate";

const getVulnerabilitiesIds: (vulnerabilities: IVulnRowAttr[]) => string[] = (
  vulnerabilities: IVulnRowAttr[]
): string[] =>
  vulnerabilities.map(
    (vulnerability: IVulnRowAttr): string => vulnerability.id
  );

const getNonSelectableVulnerabilitiesOnEdit: (
  vulnerabilities: IVulnRowAttr[]
) => number[] = (vulnerabilities: IVulnRowAttr[]): number[] =>
  vulnerabilities.reduce(
    (
      nonSelectableVulnerabilities: number[],
      vulnerabilitiy: IVulnRowAttr,
      currentVulnerabilityIndex: number
    ): number[] =>
      vulnerabilitiy.currentState === "open"
        ? nonSelectableVulnerabilities
        : [...nonSelectableVulnerabilities, currentVulnerabilityIndex],
    []
  );

const getNonSelectableVulnerabilitiesOnReattack: (
  vulnerabilities: IVulnRowAttr[]
) => number[] = (vulnerabilities: IVulnRowAttr[]): number[] =>
  vulnerabilities.reduce(
    (
      nonSelectableVulnerabilities: number[],
      vulnerabilitiy: IVulnRowAttr,
      currentVulnerabilityIndex: number
    ): number[] =>
      vulnerabilitiy.remediated || vulnerabilitiy.currentState === "closed"
        ? [...nonSelectableVulnerabilities, currentVulnerabilityIndex]
        : nonSelectableVulnerabilities,
    []
  );

const getNonSelectableVulnerabilitiesOnVerify: (
  vulnerabilities: IVulnRowAttr[]
) => number[] = (vulnerabilities: IVulnRowAttr[]): number[] =>
  vulnerabilities.reduce(
    (
      nonSelectableVulnerabilities: number[],
      vulnerabilitiy: IVulnRowAttr,
      currentVulnerabilityIndex: number
    ): number[] =>
      vulnerabilitiy.remediated && vulnerabilitiy.currentState === "open"
        ? nonSelectableVulnerabilities
        : [...nonSelectableVulnerabilities, currentVulnerabilityIndex],
    []
  );

const getVulnerabilitiesIndex: (
  selectedVulnerabilities: IVulnRowAttr[],
  allVulnerabilities: IVulnRowAttr[]
) => number[] = (
  selectedVulnerabilities: IVulnRowAttr[],
  allVulnerabilities: IVulnRowAttr[]
): number[] => {
  const selectVulnIds: string[] = getVulnerabilitiesIds(
    selectedVulnerabilities
  );

  return allVulnerabilities.reduce(
    (
      selectedVulnsIndex: number[],
      currentVulnerability: IVulnRowAttr,
      currentVulnerabilityIndex: number
    ): number[] =>
      selectVulnIds.includes(currentVulnerability.id)
        ? [...selectedVulnsIndex, currentVulnerabilityIndex]
        : selectedVulnsIndex,
    []
  );
};

const formatVulnerabilities: (
  vulnerabilities: IVulnRowAttr[]
) => IVulnRowAttr[] = (vulnerabilities: IVulnRowAttr[]): IVulnRowAttr[] =>
  vulnerabilities.map(
    (vulnerability: IVulnRowAttr): IVulnRowAttr => {
      const hasVulnCycles: boolean = _.toInteger(vulnerability.cycles) > 0;
      const lastTreatment: IHistoricTreatment = getLastTreatment(
        vulnerability.historicTreatment
      );
      const isPendingToApproval: boolean =
        lastTreatment.treatment === "ACCEPTED_UNDEFINED" &&
        lastTreatment.acceptanceStatus !== "APPROVED";
      const isVulnOpen: boolean = vulnerability.currentState === "open";
      const treatmentLabel: string =
        translate.t(formatDropdownField(lastTreatment.treatment)) +
        (isPendingToApproval
          ? translate.t(
              "search_findings.tab_description.treatment.pending_approval"
            )
          : "");

      return {
        ...vulnerability,
        currentState: _.capitalize(vulnerability.currentState),
        cycles: hasVulnCycles ? vulnerability.cycles : "",
        efficacy: hasVulnCycles ? `${vulnerability.efficacy}%` : "",
        reportDate: vulnerability.reportDate.split(" ")[0],
        treatment: isVulnOpen ? treatmentLabel : "-",
        treatmentDate: isVulnOpen ? lastTreatment.date.split(" ")[0] : "-",
        treatmentManager: isVulnOpen
          ? (lastTreatment.treatmentManager as string)
          : "-",
        verification:
          vulnerability.verification === "Verified"
            ? `${vulnerability.verification} (${vulnerability.currentState})`
            : vulnerability.verification,
        vulnType: translate.t(
          `search_findings.tab_vuln.vulnTable.vulnType.${vulnerability.vulnType}`
        ),
      };
    }
  );

export {
  formatVulnerabilities,
  getNonSelectableVulnerabilitiesOnEdit,
  getNonSelectableVulnerabilitiesOnReattack,
  getNonSelectableVulnerabilitiesOnVerify,
  getVulnerabilitiesIds,
  getVulnerabilitiesIndex,
};
