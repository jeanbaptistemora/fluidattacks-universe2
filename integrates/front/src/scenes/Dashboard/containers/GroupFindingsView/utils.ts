import type { ExecutionResult } from "graphql";
import _ from "lodash";

import type { IRemoveFindingResultAttr } from "../FindingContent/types";
import { pointStatusFormatter } from "scenes/Dashboard/components/Vulnerabilities/Formatter";
import type {
  IFindingAttr,
  IFindingData,
  ITreatmentSummaryAttr,
} from "scenes/Dashboard/containers/GroupFindingsView/types";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

type RemoveFindingResult = ExecutionResult<IRemoveFindingResultAttr>;

const formatRemediated: (remediated: string, verified: boolean) => string = (
  remediated: string,
  verified: boolean
): string =>
  translate.t(
    Boolean(remediated) || !verified
      ? "group.findings.remediated.True"
      : "group.findings.remediated.False"
  );

const formatState: (state: string) => JSX.Element = (
  state: string
): JSX.Element => {
  const stateParameters: Record<string, string> = {
    closed: "searchFindings.status.closed",
    open: "searchFindings.status.open",
  };

  return pointStatusFormatter(translate.t(stateParameters[state]));
};

const formatTreatmentSummary: (
  state: string,
  treatmentSummary: ITreatmentSummaryAttr
) => string = (
  state: string,
  treatmentSummary: ITreatmentSummaryAttr
): string =>
  state === "open"
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

const formatFindings: (dataset: IFindingAttr[]) => IFindingAttr[] = (
  findings: IFindingAttr[]
): IFindingData[] =>
  findings.map(
    (finding: IFindingAttr): IFindingData => ({
      ...finding,
      remediated: formatRemediated(finding.remediated, finding.verified),
      treatment: formatTreatmentSummary(
        finding.state,
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
  formatFindings,
  formatState,
  formatTreatmentSummary,
  formatRemediated,
  getAreAllMutationValid,
  getFindingsIndex,
  getResults,
  handleRemoveFindingsError,
  onSelectVariousFindingsHelper,
};
