import type { IHistoricTreatment } from "scenes/Dashboard/containers/DescriptionView/types";

interface IProjectFindingsAttr {
  project: {
    findings: IFindingAttr[];
  };
}

interface IFindingAttr {
  age: number;
  description: string;
  id: string;
  isExploitable: string;
  lastVulnerability: number;
  openVulnerabilities: number;
  name: string;
  remediated: string;
  severityScore: number;
  state: string;
  title: string;
  treatment: string;
  type: string;
  verified: boolean;
  vulnerabilities: {
    historicTreatment: IHistoricTreatment[];
    where: string;
    zeroRisk: string;
  }[];
}

interface IRequestProjectReportResult {
  requestProjectReport: {
    success: boolean;
  };
}

export { IProjectFindingsAttr, IFindingAttr, IRequestProjectReportResult };
