import { IHistoricTreatment } from "../DescriptionView/types";

interface IProject {
  subscription: string;
}

interface IFinding {
  historicTreatment: IHistoricTreatment[];
  id: string;
  newRemediated: boolean;
  state: "open" | "closed";
  verified: boolean;
}

interface IGetFindingVulnInfo {
  finding: IFinding;
  project: IProject;
}

export { IFinding, IGetFindingVulnInfo, IProject };
