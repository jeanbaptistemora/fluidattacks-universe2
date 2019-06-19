import { RouteComponentProps } from "react-router";

export type IIndicatorsViewBaseProps = Pick<RouteComponentProps<{ projectName: string }>, "match">;

export interface IIndicatorsProps {
  project: {
    closedVulnerabilities: number;
    currentMonthAuthors: number;
    currentMonthCommits: number;
    lastClosingVuln: number;
    maxOpenSeverity: number;
    maxSeverity: number;
    meanRemediate: number;
    openVulnerabilities: number;
    pendingClosingCheck: number;
    remediatedOverTime: string;
    totalFindings: number;
    totalTreatment: string;
  };
  resources: {
    repositories: string;
  };
}

export interface IGraphData {
  backgroundColor: string[];
  data: number[];
  hoverBackgroundColor: string[];
}
