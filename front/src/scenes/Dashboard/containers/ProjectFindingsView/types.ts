import { RouteComponentProps } from "react-router";
import { IDashboardState } from "../../reducer";

export type IProjectFindingsBaseProps = Pick<RouteComponentProps<{ projectName: string }>, "match">;

export type IProjectFindingsStateProps = IDashboardState["findings"];

export interface IProjectFindingsDispatchProps {
  onCloseReportsModal(): void;
  onOpenReportsModal(): void;
}

export interface IProjectFindingsAttr {
  project: {
    findings: Array<{
      age: number;
      description: string;
      id: string;
      isExploitable: string;
      lastVulnerability: number;
      openVulnerabilities: number;
      remediated: string;
      severityScore: number;
      state: string;
      title: string;
      treatment: string[];
      type: string;
      vulnerabilities: Array<{ where: string }>;
    }>;
  };
}

export type IProjectFindingsProps = (IProjectFindingsBaseProps &
  (IProjectFindingsStateProps & IProjectFindingsDispatchProps));
