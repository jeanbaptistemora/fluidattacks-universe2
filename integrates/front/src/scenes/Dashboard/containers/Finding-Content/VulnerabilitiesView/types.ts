import type { IHistoricTreatment } from "../DescriptionView/types";
import type { IVulnRowAttr } from "scenes/Dashboard/components/Vulnerabilities/types";

interface IVulnerabilitiesAttr {
  findingId: string;
  historicTreatment: IHistoricTreatment[];
  id: string;
  specific: string;
  state: "REJECTED" | "SAFE" | "SUBMITTED" | "VULNERABLE";
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
  status: "SAFE" | "VULNERABLE";
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
