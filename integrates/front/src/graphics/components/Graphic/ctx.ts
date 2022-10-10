/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

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
  "exposureTrendsByCategories",
  "mttrBenchmarkingNonTreatedCvssf",
  "riskOverTime",
  "riskOverTimeCvssf",
];
const allowedDocumentTypes: string[] = ["barChart", "stackedBarChart"];
const mergedDocuments: Record<string, IMergedCharts> = {
  assignedVulnerabilitiesCvssf: {
    alt: [
      {
        documentName: "assignedVulnerabilities",
        label: "Vulns",
        title: translate.t(
          "analytics.stackedBarChart.assignedVulnerabilities.altTitle"
        ),
        tooltip: translate.t(
          "analytics.stackedBarChart.assignedVulnerabilities.tooltip.vulnerabilities"
        ),
        url: "",
      },
    ],
    default: {
      documentName: "assignedVulnerabilitiesCvssf",
      label: "Exposure",
      title: translate.t(
        "analytics.stackedBarChart.assignedVulnerabilities.title"
      ),
      tooltip: translate.t(
        "analytics.stackedBarChart.assignedVulnerabilities.tooltip.cvssf"
      ),
      url: "#exposure-by-assignee",
    },
    documentType: "stackedBarChart",
  },
  distributionOverTimeCvssf: {
    alt: [
      {
        documentName: "distributionOverTime",
        label: "Vulns",
        title: translate.t(
          "analytics.stackedBarChart.distributionOverTimeCvssf.altTitle"
        ),
        tooltip: translate.t(
          "analytics.stackedBarChart.distributionOverTimeCvssf.tooltip.vulnerabilities"
        ),
        url: "",
      },
    ],
    default: {
      documentName: "distributionOverTimeCvssf",
      label: "Exposure",
      title: translate.t(
        "analytics.stackedBarChart.distributionOverTimeCvssf.title"
      ),
      tooltip: translate.t(
        "analytics.stackedBarChart.distributionOverTimeCvssf.tooltip.cvssf"
      ),
      url: "#exposure-management-over-time-",
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
      label: "Days per Exposure",
      title: translate.t("tagIndicator.meanRemediate"),
      tooltip: translate.t(
        "analytics.barChart.meanTimeToRemediate.tooltip.default"
      ),
      url: "#mean-average-days-to-remediate",
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
        url: "",
      },
    ],
    default: {
      documentName: "mttrBenchmarkingCvssf",
      label: "All",
      title: translate.t("analytics.barChart.mttrBenchmarking.title"),
      tooltip: translate.t("analytics.barChart.mttrBenchmarking.tooltip.all"),
      url: "#mean-time-to-remediate-mttr-benchmark",
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
        url: "",
      },
    ],
    default: {
      documentName: "riskOverTimeCvssf",
      label: "Exposure",
      title: translate.t("analytics.stackedBarChart.riskOverTime.title"),
      tooltip: translate.t(
        "analytics.stackedBarChart.riskOverTime.tooltip.cvssf"
      ),
      url: "#exposure-management-over-time",
    },
    documentType: "stackedBarChart",
  },
  topVulnerabilitiesCvssf: {
    alt: [
      {
        documentName: "topFindingsByVulnerabilities",
        label: "Vulns",
        title: translate.t(
          "analytics.barChart.topVulnerabilities.altTitle.vulnerabilities"
        ),
        tooltip: translate.t(
          "analytics.barChart.topVulnerabilities.tooltip.vulnerabilities"
        ),
        url: "",
      },
      {
        documentName: "topVulnerabilitiesBySourceCode",
        label: "Code",
        title: translate.t(
          "analytics.barChart.topVulnerabilities.altTitle.code"
        ),
        tooltip: translate.t(
          "analytics.barChart.topVulnerabilities.tooltip.code"
        ),
        url: "#open-exposure-by-type",
      },
      {
        documentName: "topVulnerabilitiesBySourceInfra",
        label: "Infra",
        title: translate.t(
          "analytics.barChart.topVulnerabilities.altTitle.infra"
        ),
        tooltip: translate.t(
          "analytics.barChart.topVulnerabilities.tooltip.infra"
        ),
        url: "#open-exposure-by-type",
      },
      {
        documentName: "topVulnerabilitiesBySourceApp",
        label: "App",
        title: translate.t(
          "analytics.barChart.topVulnerabilities.altTitle.app"
        ),
        tooltip: translate.t(
          "analytics.barChart.topVulnerabilities.tooltip.app"
        ),
        url: "#open-exposure-by-type",
      },
    ],
    default: {
      documentName: "topVulnerabilitiesCvssf",
      label: "Exposure",
      title: translate.t("analytics.barChart.topVulnerabilities.title"),
      tooltip: translate.t(
        "analytics.barChart.topVulnerabilities.tooltip.cvssf"
      ),
      url: "#open-exposure-by-type",
    },
    documentType: "barChart",
  },
};

export type { IDocumentValues };
export { mergedDocuments, allowedDocumentNames, allowedDocumentTypes };
