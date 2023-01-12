/* eslint @typescript-eslint/strict-boolean-expressions:0 */
/* eslint @typescript-eslint/no-unnecessary-condition:0 */
import dayjs from "dayjs";
import _ from "lodash";

import type { IVulnRowAttr } from "scenes/Dashboard/components/Vulnerabilities/types";
import type { IHistoricTreatment } from "scenes/Dashboard/containers/Finding-Content/DescriptionView/types";
import { getRequirementsText } from "scenes/Dashboard/containers/Finding-Content/DescriptionView/utils";
import type {
  IRequirementData,
  IVulnData,
} from "scenes/Dashboard/containers/Group-Content/GroupDraftsView/types";
import type { IReqFormat } from "scenes/Dashboard/containers/Group-Content/GroupVulnerabilitiesView/formatters/types";
import type { IGroups, IOrganizationGroups } from "scenes/Dashboard/types";
import { isWithInAWeek } from "utils/date";
import { formatDropdownField } from "utils/formatHelpers";
import { translate } from "utils/translations/translate";

const CRITERIA_ID_SLICE: number = 3;

const requirementsTitle = ({
  findingTitle,
  requirementsData,
  vulnsData,
}: IReqFormat): string[] => {
  const findingNumber =
    !_.isNil(findingTitle) && findingTitle
      ? findingTitle.slice(0, CRITERIA_ID_SLICE)
      : "";

  if (!_.isNil(vulnsData) && !_.isNil(findingNumber)) {
    const { requirements } = vulnsData[findingNumber] || [];

    return getRequirementsText(requirements, requirementsData);
  }

  return [];
};

const formatTreatment = (
  treatmentStatus: string,
  state: "REJECTED" | "SAFE" | "SUBMITTED" | "VULNERABLE",
  treatmentAcceptanceStatus: string | null
): string => {
  const isPendingToApproval: boolean =
    treatmentStatus === "ACCEPTED_UNDEFINED" &&
    treatmentAcceptanceStatus !== "APPROVED";
  const isVulnOpen: boolean = state === "VULNERABLE";
  const treatmentLabel: string =
    translate.t(formatDropdownField(treatmentStatus)) +
    (isPendingToApproval
      ? translate.t("searchFindings.tabDescription.treatment.pendingApproval")
      : "");

  return isVulnOpen ? treatmentLabel : "-";
};

const formatVulnerabilities: (
  vulnerabilities: IVulnRowAttr[],
  vulnsData?: Record<string, IVulnData> | undefined,
  requirementsData?: Record<string, IRequirementData> | undefined
) => IVulnRowAttr[] = (
  vulnerabilities: IVulnRowAttr[],
  vulnsData?: Record<string, IVulnData> | undefined,
  requirementsData?: Record<string, IRequirementData> | undefined
): IVulnRowAttr[] =>
  vulnerabilities.map((vulnerability: IVulnRowAttr): IVulnRowAttr => {
    const isVulnOpen: boolean = vulnerability.state === "VULNERABLE";
    const verification: string =
      vulnerability.verification === "Verified"
        ? `${vulnerability.verification} (${vulnerability.state.toLowerCase()})`
        : (vulnerability.verification as string);
    const shouldDisplayVerification: boolean =
      !_.isEmpty(vulnerability.lastVerificationDate) &&
      vulnerability.verification === "Verified"
        ? Boolean(
            isWithInAWeek(
              dayjs(vulnerability.lastVerificationDate, "YYYY-MM-DD hh:mm:ss")
            )
          )
        : true;
    const requirements: string[] = requirementsTitle({
      findingTitle: vulnerability.finding?.title,
      requirementsData,
      vulnsData,
    });

    return {
      ...vulnerability,
      assigned: isVulnOpen ? (vulnerability.treatmentAssigned as string) : "-",
      lastTreatmentDate: isVulnOpen
        ? vulnerability.lastTreatmentDate.split(" ")[0]
        : "-",
      reportDate: vulnerability.reportDate.split(" ")[0],
      requirements,
      treatmentAssigned: isVulnOpen
        ? (vulnerability.treatmentAssigned as string)
        : "-",
      treatmentDate: isVulnOpen
        ? vulnerability.lastTreatmentDate.split(" ")[0]
        : "-",
      treatmentStatus: formatTreatment(
        vulnerability.treatmentStatus,
        vulnerability.state,
        vulnerability.treatmentAcceptanceStatus
      ),
      treatmentUser: isVulnOpen ? (vulnerability.treatmentUser as string) : "-",
      verification: shouldDisplayVerification ? verification : "",
      vulnerabilityType: translate.t(
        `searchFindings.tabVuln.vulnTable.vulnerabilityType.${vulnerability.vulnerabilityType}`
      ),
    };
  });

const formatHistoricTreatment: (
  vulnerabilities: IVulnRowAttr
) => IHistoricTreatment = (vulnerability: IVulnRowAttr): IHistoricTreatment => {
  return {
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
    treatment: vulnerability.treatmentStatus,
    user: _.isNull(vulnerability.treatmentUser)
      ? ""
      : vulnerability.treatmentUser,
  };
};

const formatVulnerabilitiesTreatment: (
  vulnerabilities: IVulnRowAttr[],
  organizationsGroups: IOrganizationGroups[] | undefined
) => IVulnRowAttr[] = (
  vulnerabilities: IVulnRowAttr[],
  organizationsGroups: IOrganizationGroups[] | undefined
): IVulnRowAttr[] =>
  vulnerabilities.map((vulnerability: IVulnRowAttr): IVulnRowAttr => {
    const lastTreatment: IHistoricTreatment =
      formatHistoricTreatment(vulnerability);
    const organizationName: IOrganizationGroups | undefined =
      organizationsGroups === undefined
        ? undefined
        : organizationsGroups.find(
            (orgGroup: IOrganizationGroups): boolean =>
              orgGroup.groups.find(
                (group: IGroups): boolean =>
                  group.name === vulnerability.groupName
              )?.name === vulnerability.groupName
          );

    return {
      ...vulnerability,
      historicTreatment: [lastTreatment],
      organizationName:
        organizationName === undefined ? "" : organizationName.name,
    };
  });

function filterZeroRisk(vulnerabilities: IVulnRowAttr[]): IVulnRowAttr[] {
  return vulnerabilities.filter(
    (vuln: IVulnRowAttr): boolean =>
      _.isEmpty(vuln.zeroRisk) || vuln.zeroRisk === "Rejected"
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
      vulnerability.remediated ||
      vulnerability.state === "SAFE" ||
      vulnerability.verification?.toLowerCase() === "on_hold"
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
      vulnerability.remediated && vulnerability.state === "VULNERABLE"
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

const getVulnerabilityById: (
  vulnerabilities: IVulnRowAttr[],
  vulnerabilityId: string
) => IVulnRowAttr | undefined = (
  vulnerabilities: IVulnRowAttr[],
  vulnerabilityId: string
): IVulnRowAttr | undefined => {
  const vulns = vulnerabilities.filter(
    (vulnerability: IVulnRowAttr): boolean =>
      vulnerability.id === vulnerabilityId
  );

  return vulns.length > 0 ? vulns[0] : undefined;
};

export {
  filterOutVulnerabilities,
  filterZeroRisk,
  formatHistoricTreatment,
  formatVulnerabilities,
  formatVulnerabilitiesTreatment,
  getNonSelectableVulnerabilitiesOnReattackIds,
  getNonSelectableVulnerabilitiesOnVerifyIds,
  getVulnerabilityById,
  formatTreatment,
};
