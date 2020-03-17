import { RouteComponentProps } from "react-router";

export type IIndicatorsViewBaseProps = Pick<RouteComponentProps<{ projectName: string }>, "match">;

export interface IForcesExecution {
  strictness: string;
}

export interface IIndicatorsProps {
  forcesExecutions: {
    executions: [IForcesExecution];
  };
  project: {
    closedVulnerabilities: number;
    currentMonthAuthors: number;
    currentMonthCommits: number;
    deletionDate: string;
    hasForces: boolean;
    lastClosingVuln: number;
    maxOpenSeverity: number;
    maxSeverity: number;
    meanRemediate: number;
    openVulnerabilities: number;
    pendingClosingCheck: number;
    remediatedOverTime: string;
    totalFindings: number;
    totalTreatment: string;
    userDeletion: string;
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

export interface IRejectRemoveProject {
  rejectRemoveProject: {
    success: boolean;
  };
}
