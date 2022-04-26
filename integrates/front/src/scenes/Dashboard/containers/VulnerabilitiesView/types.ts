import type { IHistoricTreatment } from "../DescriptionView/types";
import type { IVulnRowAttr } from "scenes/Dashboard/components/Vulnerabilities/types";

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
}

interface IVulnerabilitiesAttr {
  historicTreatment: IHistoricTreatment[];
  id: string;
  specific: string;
  where: string;
  zeroRisk: string | null;
}

interface IGetFindingAndGroupInfo {
  finding: IFindingInfoAttr;
}

interface IGetFindingVulns {
  finding: IFindingVulnsAtrr;
}

interface IFindingInfoAttr {
  id: string;
  remediated: boolean;
  releaseDate: string;
  state: "closed" | "open";
  verified: boolean;
}

interface IFindingVulnsAtrr {
  vulnerabilities: IVulnRowAttr[];
  zeroRisk?: IVulnRowAttr[];
}

interface IModalConfig {
  selectedVulnerabilities: IVulnRowAttr[];
  clearSelected: () => void;
}

export type {
  IFindingAttr,
  IGetFindingVulnInfoAttr,
  IGetFindingAndGroupInfo,
  IGetFindingVulns,
  IFindingInfoAttr,
  IFindingVulnsAtrr,
  IModalConfig,
  IVulnerabilitiesAttr,
};
