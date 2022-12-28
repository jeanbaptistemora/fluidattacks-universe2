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
  findingId: string;
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

interface IVulnerabilityEdge {
  node: IVulnRowAttr;
}

interface IVulnerabilitiesConnection {
  edges: IVulnerabilityEdge[];
  pageInfo: {
    hasNextPage: boolean;
    endCursor: string;
  };
}

interface ISendNotificationResultAttr {
  sendVulnerabilityNotification: {
    success: boolean;
  };
}

export type {
  IFindingAttr,
  IGetFindingVulnInfoAttr,
  IGetFindingAndGroupInfo,
  IGetFindingVulns,
  IFindingInfoAttr,
  IFindingVulnsAtrr,
  IModalConfig,
  ISendNotificationResultAttr,
  IVulnerabilitiesAttr,
  IVulnerabilityEdge,
  IVulnerabilitiesConnection,
};
