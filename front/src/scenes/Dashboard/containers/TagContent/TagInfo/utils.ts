import { ChartData } from "chart.js";
import _ from "lodash";
import translate from "../../../../../utils/translations/translate";

export interface IStatusGraphConfig {
  closedVulnerabilities: number;
  openVulnerabilities: number;
}

export interface ITreatmentGraphConfig extends IStatusGraphConfig {
  totalTreatment: string;
}

interface IGraphConfig {
  backgroundColor: string[];
  data: number[];
  hoverBackgroundColor: string[];
  stack?: string;
}

export const calcPercent: (value: number, total: number) => number = (
  value: number,
  total: number
): number => {
  const totalPercent: number = 100;

  return _.round((value * totalPercent) / total, 1);
};

export const statusGraph: (
  graphProps: IStatusGraphConfig
) => Record<string, string | string[] | IGraphConfig[]> = (
  graphProps: IStatusGraphConfig
): Record<string, string | string[] | IGraphConfig[]> => {
  const { openVulnerabilities, closedVulnerabilities } = graphProps;
  const statusDataset: IGraphConfig = {
    backgroundColor: ["#ff1a1a", "#27BF4F"],
    data: [openVulnerabilities, closedVulnerabilities],
    hoverBackgroundColor: ["#e51414", "#069D2E"],
  };
  const totalVulnerabilities: number =
    openVulnerabilities + closedVulnerabilities;
  const openPercent: number = calcPercent(
    openVulnerabilities,
    totalVulnerabilities
  );
  const closedPercent: number = calcPercent(
    closedVulnerabilities,
    totalVulnerabilities
  );
  const statusGraphData: Record<string, string | string[] | IGraphConfig[]> = {
    datasets: [statusDataset],
    labels: [
      `${openPercent}% ${translate.t("search_findings.tab_indicators.open")}`,
      `${closedPercent}% ${translate.t(
        "search_findings.tab_indicators.closed"
      )}`,
    ],
  };

  return statusGraphData;
};

export const treatmentGraph: (props: ITreatmentGraphConfig) => ChartData = (
  props: ITreatmentGraphConfig
): ChartData => {
  const totalPercent: number = 100;
  const totalTreatment: Record<string, number> = JSON.parse(
    props.totalTreatment
  );
  const treatmentDataset: IGraphConfig = {
    backgroundColor: ["#b7b7b7", "#000", "#FFAA63", "#CD2A86"],
    data: [
      totalTreatment.accepted,
      totalTreatment.acceptedUndefined,
      totalTreatment.inProgress,
      totalTreatment.undefined,
    ],
    hoverBackgroundColor: ["#999797", "#000", "#FF9034", "#A70762"],
  };
  const acceptedPercent: number = calcPercent(
    totalTreatment.accepted,
    props.openVulnerabilities
  );
  const inProgressPercent: number = calcPercent(
    totalTreatment.inProgress,
    props.openVulnerabilities
  );
  const undefinedPercent: number = calcPercent(
    totalTreatment.undefined,
    props.openVulnerabilities
  );
  const acceptedUndefinedPercent: number = _.round(
    totalPercent - acceptedPercent - inProgressPercent - undefinedPercent,
    1
  );
  const treatmentGraphData: ChartData = {
    datasets: [treatmentDataset],
    labels: [
      `${acceptedPercent}% ${translate.t(
        "search_findings.tab_indicators.treatment_accepted"
      )}`,
      `${acceptedUndefinedPercent}% ${translate.t(
        "search_findings.tab_indicators.treatment_accepted_undefined"
      )}`,
      `${inProgressPercent}% ${translate.t(
        "search_findings.tab_indicators.treatment_in_progress"
      )}`,
      `${undefinedPercent}% ${translate.t(
        "search_findings.tab_indicators.treatment_no_defined"
      )}`,
    ],
  };

  return treatmentGraphData;
};
