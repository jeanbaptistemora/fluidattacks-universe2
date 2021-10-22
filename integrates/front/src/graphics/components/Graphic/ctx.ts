import { translate } from "utils/translations/translate";

interface IDocumentValues {
  documentName: string;
  label: string;
  title: string;
  tooltip: string;
  url: string;
}
interface IMergedCharts {
  alt: IDocumentValues[];
  default: IDocumentValues;
  documentType: string;
}

const allowedDocumentNames: string[] = [
  "meanTimeToRemediate",
  "meanTimeToRemediateCvssf",
  "mttrBenchmarkingCvssf",
  "mttrBenchmarkingNonTreatedCvssf",
  "riskOverTime",
  "riskOverTimeCvssf",
];
const allowedDocumentTypes: string[] = ["barChart", "stackedBarChart"];
const mergedDocuments: Record<string, IMergedCharts> = {
  distributionOverTimeCvssf: {
    alt: [
      {
        documentName: "distributionOverTime",
        label: "Vulns",
        title: translate.t(
          "analytics.stackedBarChart.distributionOverTimeCvssf.title"
        ),
        tooltip: translate.t(
          "analytics.stackedBarChart.distributionOverTimeCvssf.tooltip.vulnerabilities"
        ),
        url: "",
      },
    ],
    default: {
      documentName: "distributionOverTimeCvssf",
      label: "Severity",
      title: translate.t(
        "analytics.stackedBarChart.distributionOverTimeCvssf.title"
      ),
      tooltip: translate.t(
        "analytics.stackedBarChart.distributionOverTimeCvssf.tooltip.cvssf"
      ),
      url: "",
    },
    documentType: "stackedBarChart",
  },
  meanTimeToRemediateCvssf: {
    alt: [
      {
        documentName: "meanTimeToRemediate",
        label: "Days",
        title: translate.t("tagIndicator.meanRemediate"),
        tooltip: translate.t(
          "analytics.barChart.meanTimeToRemediate.tooltip.alt.default"
        ),
        url: "",
      },
      {
        documentName: "meanTimeToRemediateNonTreatedCvssf",
        label: "Non treated (CVSSF)",
        title: translate.t("tagIndicator.meanRemediate"),
        tooltip: translate.t(
          "analytics.barChart.meanTimeToRemediate.tooltip.alt.nonTreatedCvssf"
        ),
        url: "",
      },
      {
        documentName: "meanTimeToRemediateNonTreated",
        label: "Non treated days",
        title: translate.t("tagIndicator.meanRemediate"),
        tooltip: translate.t(
          "analytics.barChart.meanTimeToRemediate.tooltip.alt.nonTreated"
        ),
        url: "",
      },
    ],
    default: {
      documentName: "meanTimeToRemediateCvssf",
      label: "Days per Severity",
      title: translate.t("tagIndicator.meanRemediate"),
      tooltip: translate.t(
        "analytics.barChart.meanTimeToRemediate.tooltip.default"
      ),
      url: "",
    },
    documentType: "barChart",
  },
  mttrBenchmarkingCvssf: {
    alt: [
      {
        documentName: "mttrBenchmarkingNonTreatedCvssf",
        label: "Non treated",
        title: translate.t("analytics.barChart.mttrBenchmarking.title"),
        tooltip: translate.t(
          "analytics.barChart.mttrBenchmarking.tooltip.nonTreated"
        ),
        url: "#mean-time-to-remediate-non-treated-vulnerabilities",
      },
    ],
    default: {
      documentName: "mttrBenchmarkingNonTreatedCvssf",
      label: "All",
      title: translate.t("analytics.barChart.mttrBenchmarking.title"),
      tooltip: translate.t("analytics.barChart.mttrBenchmarking.tooltip.all"),
      url: "#mean-time-to-remediate-all-vulnerabilities",
    },
    documentType: "barChart",
  },
  riskOverTimeCvssf: {
    alt: [
      {
        documentName: "riskOverTime",
        label: "Vulns",
        title: translate.t("analytics.stackedBarChart.riskOverTime.altTitle"),
        tooltip: translate.t(
          "analytics.stackedBarChart.riskOverTime.tooltip.vulnerabilities"
        ),
        url: "#vulnerabilities-over-time",
      },
    ],
    default: {
      documentName: "riskOverTimeCvssf",
      label: "Severity",
      title: translate.t("analytics.stackedBarChart.riskOverTime.title"),
      tooltip: translate.t(
        "analytics.stackedBarChart.riskOverTime.tooltip.cvssf"
      ),
      url: "#vulnerabilities-over-time",
    },
    documentType: "stackedBarChart",
  },
  topVulnerabilitiesCvssf: {
    alt: [
      {
        documentName: "topFindingsByVulnerabilities",
        label: "Vulns",
        title: translate.t("analytics.barChart.topVulnerabilities.altTitle"),
        tooltip: translate.t(
          "analytics.barChart.topVulnerabilities.tooltip.vulnerabilities"
        ),
        url: "#top-vulnerabilities",
      },
    ],
    default: {
      documentName: "topVulnerabilitiesCvssf",
      label: "Severity",
      title: translate.t("analytics.barChart.topVulnerabilities.title"),
      tooltip: translate.t(
        "analytics.barChart.topVulnerabilities.tooltip.cvssf"
      ),
      url: "#top-vulnerabilities",
    },
    documentType: "barChart",
  },
};

export {
  mergedDocuments,
  allowedDocumentNames,
  allowedDocumentTypes,
  IDocumentValues,
};
