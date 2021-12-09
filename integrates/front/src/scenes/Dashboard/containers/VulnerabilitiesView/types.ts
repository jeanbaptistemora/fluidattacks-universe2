import type { IHistoricTreatment } from "../DescriptionView/types";
import type { IVulnRowAttr } from "scenes/Dashboard/components/Vulnerabilities/types";

interface IGroupAttr {
  subscription: string;
}

interface IFindingAttr {
  id: string;
  remediated: boolean;
  releaseDate: string;
  state: "closed" | "open";
  verified: boolean;
  vulnerabilities: IVulnRowAttr[];
  zeroRisk?: IVulnRowAttr[];
}

interface IGetFindingVulnInfoAttr {
  finding: IFindingAttr;
  group: IGroupAttr;
}

interface IVulnerabilitiesAttr {
  historicTreatment: IHistoricTreatment[];
  id: string;
  specific: string;
  where: string;
  zeroRisk: string | null;
}

export {
  IFindingAttr,
  IGetFindingVulnInfoAttr,
  IGroupAttr,
  IVulnerabilitiesAttr,
};
