import type { ExecutionResult } from "graphql";
import _ from "lodash";

import type { IRemoveFindingResultAttr } from "../../Finding-Content/types";
import { statusFormatter } from "scenes/Dashboard/components/Vulnerabilities/Formatter";
import type {
  IFindingAttr,
  ITreatmentSummaryAttr,
  IVerificationSummaryAttr,
  IVulnerabilitiesResume,
} from "scenes/Dashboard/containers/Group-Content/GroupFindingsView/types";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

type RemoveFindingResult = ExecutionResult<IRemoveFindingResultAttr>;

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
        treatmentSummary.new
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

export {
  filterAssigned,
  formatFindings,
  formatState,
  formatStatus,
  formatTreatmentSummary,
  formatReattack,
  getAreAllMutationValid,
  getFindingsIndex,
  getResults,
  handleRemoveFindingsError,
  onSelectVariousFindingsHelper,
};
