import type { IFindingAttr } from "scenes/Dashboard/containers/GroupFindingsView/types";
import { translate } from "utils/translations/translate";

const formatTreatmentSummary: (finding: IFindingAttr) => string = (
  finding: IFindingAttr
): string => `
${translate.t("searchFindings.tabDescription.treatment.new")}: ${
  finding.treatmentSummary.new
},
${translate.t("searchFindings.tabDescription.treatment.inProgress")}: ${
  finding.treatmentSummary.inProgress
},
${translate.t("searchFindings.tabDescription.treatment.accepted")}: ${
  finding.treatmentSummary.accepted
},
${translate.t("searchFindings.tabDescription.treatment.acceptedUndefined")}: ${
  finding.treatmentSummary.acceptedUndefined
}
`;

const formatFindings: (dataset: IFindingAttr[]) => IFindingAttr[] = (
  dataset: IFindingAttr[]
): IFindingAttr[] =>
  dataset.map((finding: IFindingAttr): IFindingAttr => {
    const stateParameters: Record<string, string> = {
      closed: "searchFindings.status.closed",
      open: "searchFindings.status.open",
    };
    const state: string = translate.t(stateParameters[finding.state]);
    const treatment: string =
      finding.state === "open" ? formatTreatmentSummary(finding) : "-";
    const remediated: string = translate.t(
      Boolean(finding.remediated) || !finding.verified
        ? "group.findings.remediated.True"
        : "group.findings.remediated.False"
    );

    return {
      ...finding,
      remediated,
      state,
      treatment,
    };
  });

export { formatFindings };
