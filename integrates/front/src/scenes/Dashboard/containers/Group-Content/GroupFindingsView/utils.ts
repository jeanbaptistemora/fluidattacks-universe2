import type { ExecutionResult } from "graphql";
import yaml from "js-yaml";
import _ from "lodash";

import type {
  IFindingAttr,
  IFindingSuggestionData,
  ITreatmentSummaryAttr,
  IVerificationSummaryAttr,
  IVulnerabilitiesResume,
  IVulnerabilityCriteriaData,
} from "./types";

import type { IRemoveFindingResultAttr } from "../../Finding-Content/types";
import { statusFormatter } from "scenes/Dashboard/components/Vulnerabilities/Formatter";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

type RemoveFindingResult = ExecutionResult<IRemoveFindingResultAttr>;

const ATTACK_COMPLEXITY_OPTIONS: Record<string, number> = {
  H: 0.44,
  L: 0.77,
};
/*
 * P: physical
 * L: local
 * A: adjacent
 * N: network
 */
const ATTACK_VECTOR_OPTIONS: Record<string, number> = {
  A: 0.62,
  L: 0.55,
  N: 0.85,
  P: 0.2,
};
const AVAILABILITY_IMPACT_OPTIONS: Record<string, number> = {
  H: 0.56,
  L: 0.22,
  N: 0,
};
const CONFIDENTIAL_IMPACT_OPTIONS: Record<string, number> = {
  H: 0.56,
  L: 0.22,
  N: 0,
};
/*
 * U: unproven
 * P: proof of concept
 * F: functional
 * H: high
 */
const EXPLOTABILITY_OPTIONS: Record<string, number> = {
  F: 0.97,
  H: 1,
  P: 0.94,
  U: 0.91,
};
const INTEGRITY_IMPACT_OPTIONS: Record<string, number> = {
  H: 0.56,
  L: 0.22,
  N: 0,
};
const SEVERITY_SCOPE_OPTIONS: Record<string, number> = {
  C: 1,
  U: 0,
};
const PRIVILEGES_REQUIRED_SCOPE: Record<string, number> = {
  H: 0.5,
  L: 0.68,
  N: 0.85,
};
const PRIVILEGES_REQUIRED_NO_SCOPE: Record<string, number> = {
  H: 0.27,
  L: 0.62,
  N: 0.85,
};
/*
 * O: official fix
 * T: temporary fix
 * W: workaround
 * U: unavailable
 */
const REMEDIATION_LEVEL_OPTIONS: Record<string, number> = {
  O: 0.95,
  T: 0.96,
  U: 1,
  W: 0.97,
};
/*
 * U: unknown
 * R: reasonable
 * C: confirmed
 */
const REPORT_CONFIDENCE_OPTIONS: Record<string, number> = {
  C: 1,
  R: 0.96,
  U: 0.92,
};
const USER_INTERACTIONS_OPTIONS: Record<string, number> = {
  N: 0.85,
  R: 0.62,
};

function filterAssigned(
  rows: IFindingAttr[],
  searchOption: string
): IFindingAttr[] {
  return _.isEmpty(searchOption)
    ? rows
    : rows.filter((row): boolean =>
        row.locationsInfo.treatmentAssignmentEmails.has(searchOption)
      );
}

const formatReattack: (
  verificationSummary: IVerificationSummaryAttr
) => string = (verificationSummary: IVerificationSummaryAttr): string =>
  translate.t(
    verificationSummary.requested > 0 || verificationSummary.onHold > 0
      ? "group.findings.reattack.True"
      : "group.findings.reattack.False"
  );

const formatState: (state: string) => JSX.Element = (
  state: string
): JSX.Element => {
  const stateParameters: Record<string, string> = {
    SAFE: "searchFindings.header.status.stateLabel.closed",
    VULNERABLE: "searchFindings.header.status.stateLabel.open",
    closed: "searchFindings.header.status.stateLabel.closed",
    open: "searchFindings.header.status.stateLabel.open",
  };

  return statusFormatter(translate.t(stateParameters[state]));
};

const formatStatus: (status: string) => JSX.Element = (
  status: string
): JSX.Element => {
  return statusFormatter(status, true);
};

const formatTreatmentSummary: (
  state: "SAFE" | "VULNERABLE",
  treatmentSummary: ITreatmentSummaryAttr
) => string = (
  state: "SAFE" | "VULNERABLE",
  treatmentSummary: ITreatmentSummaryAttr
): string =>
  state === "VULNERABLE"
    ? `
${translate.t("searchFindings.tabDescription.treatment.new")}: ${
        treatmentSummary.untreated
      },
${translate.t("searchFindings.tabDescription.treatment.inProgress")}: ${
        treatmentSummary.inProgress
      },
${translate.t("searchFindings.tabDescription.treatment.accepted")}: ${
        treatmentSummary.accepted
      },
${translate.t("searchFindings.tabDescription.treatment.acceptedUndefined")}: ${
        treatmentSummary.acceptedUndefined
      }
`
    : "-";

const formatClosingPercentage = (finding: IFindingAttr): number => {
  const { closedVulnerabilities, openVulnerabilities }: IFindingAttr = finding;

  if (openVulnerabilities + closedVulnerabilities === 0) {
    return finding.status === "SAFE" ? 1.0 : 0;
  }

  return closedVulnerabilities / (openVulnerabilities + closedVulnerabilities);
};

const formatFindings = (
  findings: IFindingAttr[],
  findingLocations: Record<string, IVulnerabilitiesResume>
): IFindingAttr[] =>
  findings.map(
    (finding): IFindingAttr => ({
      ...finding,
      closingPercentage: formatClosingPercentage(finding),
      locationsInfo: {
        closedVulnerabilities: finding.closedVulnerabilities,
        findingId: finding.id,
        locations: _.get(findingLocations, finding.id, undefined)?.wheres,
        openVulnerabilities: finding.openVulnerabilities,
        treatmentAssignmentEmails:
          _.get(findingLocations, finding.id, undefined)
            ?.treatmentAssignmentEmails ?? new Set([]),
      },
      reattack: formatReattack(finding.verificationSummary),
      treatment: formatTreatmentSummary(
        finding.status,
        finding.treatmentSummary
      ),
    })
  );

const getAreAllMutationValid = (
  results: ExecutionResult<IRemoveFindingResultAttr>[]
): boolean[] => {
  return results.map(
    (result: ExecutionResult<IRemoveFindingResultAttr>): boolean => {
      if (!_.isUndefined(result.data) && !_.isNull(result.data)) {
        const removeInfoSuccess: boolean = _.isUndefined(
          result.data.removeFinding
        )
          ? true
          : result.data.removeFinding.success;

        return removeInfoSuccess;
      }

      return false;
    }
  );
};

const getFindingsIds: (vulnerabilities: IFindingAttr[]) => string[] = (
  vulnerabilities: IFindingAttr[]
): string[] =>
  vulnerabilities.map(
    (vulnerability: IFindingAttr): string => vulnerability.id
  );

const getFindingsIndex: (
  selectedFindings: IFindingAttr[],
  allFindings: IFindingAttr[]
) => number[] = (
  selectedFindings: IFindingAttr[],
  allFindings: IFindingAttr[]
): number[] => {
  const selectFindingIds: string[] = getFindingsIds(selectedFindings);

  return allFindings.reduce(
    (
      selectedFindingsIndex: number[],
      currentFinding: IFindingAttr,
      currentFindingIndex: number
    ): number[] =>
      selectFindingIds.includes(currentFinding.id)
        ? [...selectedFindingsIndex, currentFindingIndex]
        : selectedFindingsIndex,
    []
  );
};

const getResults = async (
  removeFinding: (
    variables: Record<string, unknown>
  ) => Promise<RemoveFindingResult>,
  findings: IFindingAttr[],
  justification: unknown
): Promise<RemoveFindingResult[]> => {
  const chunkSize = 10;
  const vulnChunks = _.chunk(findings, chunkSize);
  const updateChunks = vulnChunks.map(
    (chunk): (() => Promise<RemoveFindingResult[]>) =>
      async (): Promise<RemoveFindingResult[]> => {
        const updates = chunk.map(
          async (finding): Promise<RemoveFindingResult> =>
            removeFinding({
              variables: { findingId: finding.id, justification },
            })
        );

        return Promise.all(updates);
      }
  );

  // Sequentially execute chunks
  return updateChunks.reduce(
    async (previousValue, currentValue): Promise<RemoveFindingResult[]> => [
      ...(await previousValue),
      ...(await currentValue()),
    ],
    Promise.resolve<RemoveFindingResult[]>([])
  );
};

const handleRemoveFindingsError = (updateError: unknown): void => {
  if (
    _.includes(
      String(updateError),
      translate.t("searchFindings.tabVuln.exceptions.sameValues")
    )
  ) {
    msgError(translate.t("searchFindings.tabVuln.exceptions.sameValues"));
  } else {
    msgError(translate.t("groupAlerts.errorTextsad"));
    Logger.warning("An error occurred removing findings", updateError);
  }
};

const onSelectVariousFindingsHelper = (
  isSelect: boolean,
  findingsSelected: IFindingAttr[],
  selectedFindings: IFindingAttr[],
  setSelectedFindings: (value: React.SetStateAction<IFindingAttr[]>) => void
): string[] => {
  if (isSelect) {
    const findingsToSet: IFindingAttr[] = Array.from(
      new Set([...selectedFindings, ...findingsSelected])
    );
    setSelectedFindings(findingsToSet);

    return findingsToSet.map((finding: IFindingAttr): string => finding.id);
  }
  const findingsIds: string[] = getFindingsIds(findingsSelected);
  setSelectedFindings(
    Array.from(
      new Set(
        selectedFindings.filter(
          (selectedFinding: IFindingAttr): boolean =>
            !findingsIds.includes(selectedFinding.id)
        )
      )
    )
  );

  return selectedFindings.map((finding: IFindingAttr): string => finding.id);
};

const getRiskExposure = (
  status: string,
  severityScore: number,
  groupCVSSF: number
): number => {
  if (status === "SAFE") return 0;

  return 4 ** (severityScore - 4) / groupCVSSF;
};

// Empty fields in criteria's data.yaml are filled with "__empty__" or "X"
function validateNotEmpty(field: string | undefined): string {
  if (!_.isNil(field) && field !== "__empty__" && field !== "X") {
    return field;
  }

  return "";
}

function getPrivilegesRequired(
  severityScope: number,
  privilegesRequired: string
): number {
  if (severityScope === SEVERITY_SCOPE_OPTIONS.C) {
    return PRIVILEGES_REQUIRED_SCOPE[privilegesRequired];
  }

  return PRIVILEGES_REQUIRED_NO_SCOPE[privilegesRequired];
}

async function getFindingSuggestions(): Promise<IFindingSuggestionData[]> {
  const baseUrl: string =
    "https://gitlab.com/api/v4/projects/20741933/repository/files";
  const branchRef: string = "trunk";
  const vulnsFileId: string =
    "common%2Fcriteria%2Fsrc%2Fvulnerabilities%2Fdata.yaml";
  const vulnsResponseFile: Response = await fetch(
    `${baseUrl}/${vulnsFileId}/raw?ref=${branchRef}`
  );
  const vulnsData = yaml.load(await vulnsResponseFile.text()) as Record<
    string,
    IVulnerabilityCriteriaData
  >;

  return Object.keys(vulnsData).map((key: string): IFindingSuggestionData => {
    const attackVectorRaw = validateNotEmpty(
      vulnsData[key].score.base.attack_vector
    );
    const attackVector =
      attackVectorRaw in ATTACK_VECTOR_OPTIONS
        ? ATTACK_VECTOR_OPTIONS[attackVectorRaw]
        : 0;
    const attackComplexityRaw = validateNotEmpty(
      vulnsData[key].score.base.attack_complexity
    );
    const attackComplexity =
      attackComplexityRaw in ATTACK_COMPLEXITY_OPTIONS
        ? ATTACK_COMPLEXITY_OPTIONS[attackComplexityRaw]
        : 0;
    const availabilityRaw = validateNotEmpty(
      vulnsData[key].score.base.availability
    );
    const availabilityImpact =
      availabilityRaw in AVAILABILITY_IMPACT_OPTIONS
        ? AVAILABILITY_IMPACT_OPTIONS[availabilityRaw]
        : 0;
    const confidentialityRaw = validateNotEmpty(
      vulnsData[key].score.base.confidentiality
    );
    const confidentialityImpact =
      confidentialityRaw in CONFIDENTIAL_IMPACT_OPTIONS
        ? CONFIDENTIAL_IMPACT_OPTIONS[confidentialityRaw]
        : 0;
    const exploitabilityRaw = validateNotEmpty(
      vulnsData[key].score.temporal.exploit_code_maturity
    );
    const exploitability =
      exploitabilityRaw in EXPLOTABILITY_OPTIONS
        ? EXPLOTABILITY_OPTIONS[exploitabilityRaw]
        : 0;
    const integrityRaw = validateNotEmpty(vulnsData[key].score.base.integrity);
    const integrityImpact =
      integrityRaw in INTEGRITY_IMPACT_OPTIONS
        ? INTEGRITY_IMPACT_OPTIONS[integrityRaw]
        : 0;
    const scopeRaw = validateNotEmpty(vulnsData[key].score.base.scope);
    const severityScope =
      scopeRaw in SEVERITY_SCOPE_OPTIONS ? SEVERITY_SCOPE_OPTIONS[scopeRaw] : 0;
    const privilegesRequiredRaw = validateNotEmpty(
      vulnsData[key].score.base.privileges_required
    );
    const privilegesRequired =
      privilegesRequiredRaw in PRIVILEGES_REQUIRED_SCOPE
        ? getPrivilegesRequired(severityScope, privilegesRequiredRaw)
        : 0;
    const minTimeToRemediateRaw = validateNotEmpty(
      vulnsData[key].remediation_time
    );
    const minTimeToRemediate = minTimeToRemediateRaw
      ? _.parseInt(minTimeToRemediateRaw)
      : null;
    const remediationLevelRaw = validateNotEmpty(
      vulnsData[key].score.temporal.remediation_level
    );
    const remediationLevel =
      remediationLevelRaw in REMEDIATION_LEVEL_OPTIONS
        ? REMEDIATION_LEVEL_OPTIONS[remediationLevelRaw]
        : 0;
    const reportConfidenceRaw = validateNotEmpty(
      vulnsData[key].score.temporal.report_confidence
    );
    const reportConfidence =
      reportConfidenceRaw in REPORT_CONFIDENCE_OPTIONS
        ? REPORT_CONFIDENCE_OPTIONS[reportConfidenceRaw]
        : 0;
    const userInteractionRaw = validateNotEmpty(
      vulnsData[key].score.base.user_interaction
    );
    const userInteraction =
      userInteractionRaw in USER_INTERACTIONS_OPTIONS
        ? USER_INTERACTIONS_OPTIONS[userInteractionRaw]
        : 0;
    const { requirements } = vulnsData[key];

    return {
      attackComplexity,
      attackVector,
      attackVectorDescription: validateNotEmpty(vulnsData[key].en.impact),
      availabilityImpact,
      code: key,
      confidentialityImpact,
      description: validateNotEmpty(vulnsData[key].en.description),
      exploitability,
      integrityImpact,
      minTimeToRemediate,
      privilegesRequired,
      recommendation: validateNotEmpty(vulnsData[key].en.recommendation),
      remediationLevel,
      reportConfidence,
      severityScope,
      threat: validateNotEmpty(vulnsData[key].en.threat),
      title: validateNotEmpty(vulnsData[key].en.title),
      unfulfilledRequirements: requirements,
      userInteraction,
    };
  });
}

export {
  filterAssigned,
  formatFindings,
  formatState,
  formatStatus,
  formatTreatmentSummary,
  formatReattack,
  getAreAllMutationValid,
  getFindingsIndex,
  getFindingSuggestions,
  getResults,
  getRiskExposure,
  handleRemoveFindingsError,
  onSelectVariousFindingsHelper,
};
