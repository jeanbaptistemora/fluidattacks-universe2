import { translate } from "utils/translations/translate";

interface IDocumentValues {
  label: string;
  title: string;
  tooltip: string;
  url: string;
}
interface IMergedCharts {
  alt: IDocumentValues;
  default: IDocumentValues;
  documentName: string;
  documentType: string;
}

const allowedDocumentNames: string[] = ["riskOverTime", "riskOverTimeCvssf"];
const allowedDocumentTypes: string[] = [
  "barChart",
  "stackedBarChart",
  "textBox",
];
const mergedDocuments: Record<string, IMergedCharts> = {
  distributionOverTimeCvssf: {
    alt: {
      label: "Vulns",
      title: translate.t(
        "analytics.stackedBarChart.distributionOverTimeCvssf.title"
      ),
      tooltip: translate.t(
        "analytics.stackedBarChart.distributionOverTimeCvssf.tooltip.vulnerabilities"
      ),
      url: "",
    },
    default: {
      label: "Cvssf",
      title: translate.t(
        "analytics.stackedBarChart.distributionOverTimeCvssf.title"
      ),
      tooltip: translate.t(
        "analytics.stackedBarChart.distributionOverTimeCvssf.tooltip.cvssf"
      ),
      url: "",
    },
    documentName: "distributionOverTime",
    documentType: "stackedBarChart",
  },
  mttrBenchmarking: {
    alt: {
      label: "Non treated",
      title: translate.t("analytics.barChart.mttrBenchmarking.title"),
      tooltip: translate.t(
        "analytics.barChart.mttrBenchmarking.tooltip.nonTreated"
      ),
      url: "",
    },
    default: {
      label: "All",
      title: translate.t("analytics.barChart.mttrBenchmarking.title"),
      tooltip: translate.t("analytics.barChart.mttrBenchmarking.tooltip.all"),
      url: "",
    },
    documentName: "mttrBenchmarkingNonTreated",
    documentType: "barChart",
  },
  riskOverTimeCvssf: {
    alt: {
      label: "Vulns",
      title: translate.t("analytics.stackedBarChart.riskOverTime.altTitle"),
      tooltip: translate.t(
        "analytics.stackedBarChart.riskOverTime.tooltip.vulnerabilities"
      ),
      url: "#vulnerabilities-over-time",
    },
    default: {
      label: "Cvssf",
      title: translate.t("analytics.stackedBarChart.riskOverTime.title"),
      tooltip: translate.t(
        "analytics.stackedBarChart.riskOverTime.tooltip.cvssf"
      ),
      url: "#vulnerabilities-over-time",
    },
    documentName: "riskOverTime",
    documentType: "stackedBarChart",
  },
  topVulnerabilitiesCvssf: {
    alt: {
      label: "Vulns",
      title: translate.t("analytics.barChart.topVulnerabilities.title"),
      tooltip: translate.t(
        "analytics.barChart.topVulnerabilities.tooltip.vulnerabilities"
      ),
      url: "#top-vulnerabilities",
    },
    default: {
      label: "Cvssf",
      title: translate.t("analytics.barChart.topVulnerabilities.title"),
      tooltip: translate.t(
        "analytics.barChart.topVulnerabilities.tooltip.cvssf"
      ),
      url: "#top-vulnerabilities",
    },
    documentName: "topFindingsByVulnerabilities",
    documentType: "barChart",
  },
};

export { mergedDocuments, allowedDocumentNames, allowedDocumentTypes };
