import { RouteComponentProps } from "react-router";
import { IHistoricTreatment } from "../DescriptionView/types";

export type IProjectFindingsProps = RouteComponentProps<{ projectName: string }>;

export interface IProjectFindingsAttr {
  project: {
    findings: IFindingAttr[];
  };
}

export interface IFindingAttr {
  age: number;
  description: string;
  historicTreatment: IHistoricTreatment[];
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
  vulnerabilities: Array<{ where: string }>;
}
