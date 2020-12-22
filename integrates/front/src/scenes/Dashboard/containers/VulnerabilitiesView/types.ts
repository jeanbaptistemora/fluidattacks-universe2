import type { IHistoricTreatment } from "../DescriptionView/types";

interface IProject {
  subscription: string;
}

interface IFinding {
  id: string;
  newRemediated: boolean;
  state: "open" | "closed";
  verified: boolean;
  vulnerabilities: IVulnerabilities[];
}

interface IGetFindingVulnInfo {
  finding: IFinding;
  project: IProject;
}

interface IVulnerabilities {
  historicTreatment: IHistoricTreatment[];
  id: string;
  specific: string;
  where: string;
  zeroRisk: string;
}

export { IFinding, IGetFindingVulnInfo, IProject, IVulnerabilities };
