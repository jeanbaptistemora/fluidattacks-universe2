import { IHistoricTreatment } from "scenes/Dashboard/containers/DescriptionView/types";

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
  vulnerabilities: Array<{
    historicTreatment: IHistoricTreatment[];
    where: string;
    zeroRisk: string;
  }>;
}

export interface IRequestProjectReportResult {
  requestProjectReport: {
    success: boolean;
  };
}
