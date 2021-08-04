import { translate } from "utils/translations/translate";

interface IDocumentValues {
  label: string;
  tooltip: string;
  url: string;
}
interface IMergedCharts {
  alt: IDocumentValues;
  default: IDocumentValues;
  documentName: string;
  documentType: string;
}

const allowedDocumentNames: string[] = [
  "meanTimeToRemediate",
  "meanTimeToRemediateNonTreated",
  "riskOverTime",
];
const allowedDocumentTypes: string[] = [
  "barChart",
  "stackedBarChart",
  "textBox",
];
const mergedDocuments: Record<string, IMergedCharts> = {
  meanTimeToRemediate: {
    alt: {
      label: "Non treated",
      tooltip: translate.t(
        "analytics.textBox.meanTimeToRemediate.tooltip.nonTreated"
      ),
      url: "#mean-time-to-remediate-non-treated-vulnerabilities",
    },
    default: {
      label: "All",
      tooltip: translate.t("analytics.textBox.meanTimeToRemediate.tooltip.all"),
      url: "#mean-time-to-remediate-all-vulnerabilities",
    },
    documentName: "meanTimeToRemediateNonTreated",
    documentType: "textBox",
  },
};

export { mergedDocuments, allowedDocumentNames, allowedDocumentTypes };
