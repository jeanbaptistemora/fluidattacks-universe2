import _ from "lodash";
import moment from "moment";

import { pointStatusFormatter } from "scenes/Dashboard/components/Vulnerabilities/Formatter";
import type {
  IFindingAttr,
  IFindingData,
  ITreatmentSummaryAttr,
} from "scenes/Dashboard/containers/GroupFindingsView/types";
import { translate } from "utils/translations/translate";

const formatRemediated: (remediated: string, verified: boolean) => string = (
  remediated: string,
  verified: boolean
): string =>
  translate.t(
    Boolean(remediated) || !verified
      ? "group.findings.remediated.True"
      : "group.findings.remediated.False"
  );

const formatReport: (date: string) => number = (date: string): number => {
  if (_.isEmpty(date)) {
    return 0;
  }

  return moment().diff(moment(date), "days");
};

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
      lastReport: formatReport(finding.lastVulnerabilityReportDate),
      openAge: formatReport(finding.oldestOpenVulnerabilityReportDate),
      remediated: formatRemediated(finding.remediated, finding.verified),
      treatment: formatTreatmentSummary(
        finding.state,
        finding.treatmentSummary
      ),
    })
  );

export {
  formatFindings,
  formatReport,
  formatState,
  formatTreatmentSummary,
  formatRemediated,
};
