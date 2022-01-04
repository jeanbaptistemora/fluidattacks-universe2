import _ from "lodash";
import moment from "moment";

import type { IVulnRowAttr } from "scenes/Dashboard/components/Vulnerabilities/types";
import type { IHistoricTreatment } from "scenes/Dashboard/containers/DescriptionView/types";
import { isWithInAWeek } from "utils/date";
import { formatDropdownField } from "utils/formatHelpers";
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
  vulnerabilities.map((vulnerability: IVulnRowAttr): IVulnRowAttr => {
    const isPendingToApproval: boolean =
      vulnerability.treatment === "ACCEPTED_UNDEFINED" &&
      vulnerability.treatmentAcceptanceStatus !== "APPROVED";
    const isVulnOpen: boolean = vulnerability.currentState === "open";
    const treatmentLabel: string =
      translate.t(formatDropdownField(vulnerability.treatment)) +
      (isPendingToApproval
        ? translate.t("searchFindings.tabDescription.treatment.pendingApproval")
        : "");
    const verification: string =
      vulnerability.verification === "Verified"
        ? `${vulnerability.verification} (${vulnerability.currentState})`
        : (vulnerability.verification as string);
    const shouldDisplayVerification: boolean =
      !_.isEmpty(vulnerability.lastVerificationDate) &&
      vulnerability.verification === "Verified"
        ? Boolean(
            isWithInAWeek(
              moment(vulnerability.lastVerificationDate, "YYYY-MM-DD hh:mm:ss")
            )
          )
        : true;

    return {
      ...vulnerability,
      assigned: isVulnOpen ? (vulnerability.treatmentAssigned as string) : "-",
      currentStateCapitalized: _.capitalize(
        vulnerability.currentState
      ) as IVulnRowAttr["currentStateCapitalized"],
      lastTreatmentDate: isVulnOpen
        ? vulnerability.lastTreatmentDate.split(" ")[0]
        : "-",
      reportDate: vulnerability.reportDate.split(" ")[0],
      treatment: isVulnOpen ? treatmentLabel : "-",
      treatmentAssigned: isVulnOpen
        ? (vulnerability.treatmentAssigned as string)
        : "-",
      treatmentDate: isVulnOpen
        ? vulnerability.lastTreatmentDate.split(" ")[0]
        : "-",
      verification: shouldDisplayVerification ? verification : "",
      vulnerabilityType: translate.t(
        `searchFindings.tabVuln.vulnTable.vulnerabilityType.${vulnerability.vulnerabilityType}`
      ),
    };
  });

const formatVulnerabilitiesTreatment: (
  vulnerabilities: IVulnRowAttr[]
) => IVulnRowAttr[] = (vulnerabilities: IVulnRowAttr[]): IVulnRowAttr[] =>
  vulnerabilities.map((vulnerability: IVulnRowAttr): IVulnRowAttr => {
    const lastTreatment: IHistoricTreatment = {
      acceptanceDate: _.isNull(vulnerability.treatmentAcceptanceDate)
        ? undefined
        : vulnerability.treatmentAcceptanceDate,
      acceptanceStatus: _.isNull(vulnerability.treatmentAcceptanceStatus)
        ? undefined
        : vulnerability.treatmentAcceptanceStatus,
      assigned: _.isNull(vulnerability.treatmentAssigned)
        ? undefined
        : vulnerability.treatmentAssigned,
      date: vulnerability.lastTreatmentDate,
      justification: _.isNull(vulnerability.treatmentJustification)
        ? undefined
        : vulnerability.treatmentJustification,
      treatment: vulnerability.treatment,
      user: "",
    };

    return {
      ...vulnerability,
      historicTreatment: [lastTreatment],
    };
  });

function filterZeroRisk(vulnerabilities: IVulnRowAttr[]): IVulnRowAttr[] {
  return vulnerabilities.filter(
    (vuln: IVulnRowAttr): boolean =>
      _.isEmpty(vuln.zeroRisk) || vuln.zeroRisk === "Rejected"
  );
}

function filterTreatment(
  vulnerabilities: IVulnRowAttr[],
  treatment: string
): IVulnRowAttr[] {
  return vulnerabilities.filter((vuln: IVulnRowAttr): boolean =>
    _.isEmpty(treatment)
      ? true
      : vuln.treatment === treatment && vuln.currentState === "open"
  );
}
function filterVerification(
  vulnerabilities: IVulnRowAttr[],
  verification: string
): IVulnRowAttr[] {
  return vulnerabilities.filter((vuln: IVulnRowAttr): boolean =>
    _.isEmpty(verification) ? true : vuln.verification === verification
  );
}
function filterCurrentStatus(
  vulnerabilities: IVulnRowAttr[],
  currentState: string
): IVulnRowAttr[] {
  return vulnerabilities.filter((vuln: IVulnRowAttr): boolean =>
    _.isEmpty(currentState) ? true : vuln.currentState === currentState
  );
}
function filterReportDate(
  vulnerabilities: IVulnRowAttr[],
  currentDate: string
): IVulnRowAttr[] {
  const selectedDate = new Date(currentDate);

  return vulnerabilities.filter((vuln: IVulnRowAttr): boolean => {
    const reportDate = new Date(vuln.reportDate);

    return _.isEmpty(currentDate)
      ? true
      : selectedDate.getUTCDate() === reportDate.getDate() &&
          selectedDate.getUTCMonth() === reportDate.getMonth() &&
          selectedDate.getUTCFullYear() === reportDate.getFullYear();
  });
}
function filterTag(
  vulnerabilities: IVulnRowAttr[],
  currentTag: string
): IVulnRowAttr[] {
  return vulnerabilities.filter((vuln: IVulnRowAttr): boolean =>
    _.isEmpty(currentTag)
      ? true
      : _.includes(vuln.tag.toLowerCase(), currentTag.toLowerCase())
  );
}
function filterTreatmentCurrentStatus(
  vulnerabilities: IVulnRowAttr[],
  currentState: string
): IVulnRowAttr[] {
  return vulnerabilities.filter((vuln: IVulnRowAttr): boolean => {
    const isPendingToApproval: string = (
      vuln.treatment === "ACCEPTED_UNDEFINED" &&
      vuln.treatmentAcceptanceStatus !== "APPROVED"
    ).toString();

    return _.isEmpty(currentState)
      ? true
      : isPendingToApproval === currentState;
  });
}
function filterText(
  vulnerabilities: IVulnRowAttr[],
  searchText: string
): IVulnRowAttr[] {
  return vulnerabilities.filter((vuln: IVulnRowAttr): boolean =>
    _.isEmpty(searchText)
      ? true
      : _.some(vuln, (value: unknown): boolean =>
          _.isString(value)
            ? _.includes(value.toLowerCase(), searchText.toLowerCase())
            : false
        )
  );
}

function getNonSelectableVulnerabilitiesOnReattackIds(
  vulnerabilities: IVulnRowAttr[]
): string[] {
  return vulnerabilities.reduce(
    (
      nonSelectableVulnerabilities: string[],
      vulnerability: IVulnRowAttr
    ): string[] =>
      vulnerability.remediated || vulnerability.currentState === "closed"
        ? [...nonSelectableVulnerabilities, vulnerability.id]
        : nonSelectableVulnerabilities,
    []
  );
}

function getNonSelectableVulnerabilitiesOnVerifyIds(
  vulnerabilities: IVulnRowAttr[]
): string[] {
  return vulnerabilities.reduce(
    (
      nonSelectableVulnerabilities: string[],
      vulnerability: IVulnRowAttr
    ): string[] =>
      vulnerability.remediated && vulnerability.currentState === "open"
        ? nonSelectableVulnerabilities
        : [...nonSelectableVulnerabilities, vulnerability.id],
    []
  );
}

function filterOutVulnerabilities(
  selectedVulnerabilities: IVulnRowAttr[],
  allVulnerabilities: IVulnRowAttr[],
  filter: (vulnerabilities: IVulnRowAttr[]) => string[]
): IVulnRowAttr[] {
  return Array.from(
    new Set(
      selectedVulnerabilities.filter(
        (selectedVulnerability: IVulnRowAttr): boolean =>
          !filter(allVulnerabilities).includes(selectedVulnerability.id)
      )
    )
  );
}

export {
  filterVerification,
  filterText,
  filterTreatment,
  filterCurrentStatus,
  filterOutVulnerabilities,
  filterReportDate,
  filterTag,
  filterTreatmentCurrentStatus,
  filterZeroRisk,
  formatVulnerabilities,
  formatVulnerabilitiesTreatment,
  getNonSelectableVulnerabilitiesOnEdit,
  getNonSelectableVulnerabilitiesOnReattack,
  getNonSelectableVulnerabilitiesOnReattackIds,
  getNonSelectableVulnerabilitiesOnVerify,
  getNonSelectableVulnerabilitiesOnVerifyIds,
  getVulnerabilitiesIds,
  getVulnerabilitiesIndex,
};
