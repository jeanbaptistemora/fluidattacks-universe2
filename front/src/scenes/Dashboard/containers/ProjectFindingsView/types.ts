import { RouteComponentProps } from "react-router";
import { IDashboardState } from "../../reducer";
import { IHistoricTreatment } from "../DescriptionView/types";

export type IProjectFindingsBaseProps = Pick<RouteComponentProps<{ projectName: string }>, "match">;

export type IProjectFindingsStateProps = IDashboardState["findings"];

export interface IProjectFindingsDispatchProps {
  onCloseReportsModal(): void;
  onFilter(newValues: {}): void;
  onOpenReportsModal(): void;
  onSort(newValues: {}): void;
}

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

export type IProjectFindingsProps = (IProjectFindingsBaseProps &
  (IProjectFindingsStateProps & IProjectFindingsDispatchProps));
