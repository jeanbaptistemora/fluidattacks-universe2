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
  "riskOverTimeCvssf",
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
  riskOverTimeCvssf: {
    alt: {
      label: "Vulns",
      tooltip: translate.t(
        "analytics.stackedBarChart.riskOverTime.tooltip.vulnerabilities"
      ),
      url: "#vulnerabilities-over-time",
    },
    default: {
      label: "Cvssf",
      tooltip: translate.t(
        "analytics.stackedBarChart.riskOverTime.tooltip.cvssf"
      ),
      url: "#vulnerabilities-over-time",
    },
    documentName: "riskOverTime",
    documentType: "stackedBarChart",
  },
};

export { mergedDocuments, allowedDocumentNames, allowedDocumentTypes };
