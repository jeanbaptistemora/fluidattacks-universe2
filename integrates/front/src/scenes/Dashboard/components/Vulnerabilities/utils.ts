import type { IHistoricTreatment } from "scenes/Dashboard/containers/DescriptionView/types";
import type { IVulnRowAttr } from "scenes/Dashboard/components/Vulnerabilities/types";
import _ from "lodash";
import { formatDropdownField } from "utils/formatHelpers";
import { getLastTreatment } from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription/utils";
import { isWithInAWeek } from "utils/utils";
import moment from "moment";
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
      const firstTreatment: IHistoricTreatment =
        vulnerability.historicTreatment[0];
      const treatmentChanges: number =
        vulnerability.historicTreatment.length -
        (firstTreatment.treatment === "NEW" ? 1 : 0);
      const verification: string =
        vulnerability.verification === "Verified"
          ? `${vulnerability.verification} (${vulnerability.currentState})`
          : vulnerability.verification;
      const shouldDisplayVerification: boolean =
        !_.isEmpty(vulnerability.lastReattackDate) &&
        vulnerability.verification === "Verified"
          ? isWithInAWeek(
              moment(vulnerability.lastReattackDate, "YYYY-MM-DD hh:mm:ss")
            )
            ? true
            : false
          : true;

      return {
        ...vulnerability,
        currentStateCapitalized: _.capitalize(
          vulnerability.currentState
        ) as IVulnRowAttr["currentStateCapitalized"],
        cycles: hasVulnCycles ? vulnerability.cycles : "",
        efficacy: hasVulnCycles ? `${vulnerability.efficacy}%` : "",
        reportDate: vulnerability.reportDate.split(" ")[0],
        treatment: isVulnOpen ? treatmentLabel : "-",
        treatmentChanges: treatmentChanges,
        treatmentDate: isVulnOpen ? lastTreatment.date.split(" ")[0] : "-",
        treatmentManager: isVulnOpen
          ? (lastTreatment.treatmentManager as string)
          : "-",
        verification: shouldDisplayVerification ? verification : "",
        vulnType: translate.t(
          `search_findings.tab_vuln.vulnTable.vulnType.${vulnerability.vulnType}`
        ),
      };
    }
  );

function filterZeroRisk(vulnerabilities: IVulnRowAttr[]): IVulnRowAttr[] {
  return vulnerabilities.filter(
    (vuln: IVulnRowAttr): boolean =>
      vuln.zeroRisk === "" || vuln.zeroRisk === "Rejected"
  );
}

export {
  filterZeroRisk,
  formatVulnerabilities,
  getNonSelectableVulnerabilitiesOnEdit,
  getNonSelectableVulnerabilitiesOnReattack,
  getNonSelectableVulnerabilitiesOnVerify,
  getVulnerabilitiesIds,
  getVulnerabilitiesIndex,
};
