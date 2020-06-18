import { RouteComponentProps } from "react-router";
import { IFindingAttr } from "../ProjectFindingsView/types";

export type IIndicatorsViewBaseProps = Pick<RouteComponentProps<{ projectName: string }>, "match">;

export interface IIndicatorsProps {
  project: {
    closedVulnerabilities: number;
    currentMonthAuthors: number;
    currentMonthCommits: number;
    deletionDate: string;
    hasForces: boolean;
    lastClosingVuln: number;
    lastClosingVulnFinding: IFindingAttr;
    maxOpenSeverity: number;
    maxOpenSeverityFinding: IFindingAttr;
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

export interface IRejectRemoveProject {
  rejectRemoveProject: {
    success: boolean;
  };
}
