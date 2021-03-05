import type { IHistoricTreatment } from "../DescriptionView/types";
import type { IVulnRowAttr } from "scenes/Dashboard/components/Vulnerabilities/types";

interface IProjectAttr {
  subscription: string;
}

interface IFindingAttr {
  id: string;
  newRemediated: boolean;
  releaseDate: string;
  state: "closed" | "open";
  verified: boolean;
  vulnerabilities: IVulnRowAttr[];
  zeroRisk?: IVulnRowAttr[];
}

interface IGetFindingVulnInfoAttr {
  finding: IFindingAttr;
  project: IProjectAttr;
}

interface IVulnerabilitiesAttr {
  historicTreatment: IHistoricTreatment[];
  id: string;
  specific: string;
  where: string;
  zeroRisk: string;
}

export {
  IFindingAttr,
  IGetFindingVulnInfoAttr,
  IProjectAttr,
  IVulnerabilitiesAttr,
};
