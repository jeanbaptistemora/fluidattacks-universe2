import { RouteComponentProps } from "react-router";
import { IHistoricTreatment } from "scenes/Dashboard/containers/DescriptionView/types";

export type IProjectFindingsProps = RouteComponentProps<{ projectName: string }>;

export interface IProjectFindingsAttr {
  project: {
    findings: IFindingAttr[];
  };
}

export interface IFindingAttr {
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
  treatment: string;
  type: string;
  verified: boolean;
  vulnerabilities: Array<{ historicTreatment: IHistoricTreatment[]; where: string  }>;
}

export interface IRequestProjectReportResult {
  requestProjectReport: {
    success: boolean;
  };
}
