import type { IHistoricTreatment } from "scenes/Dashboard/containers/DescriptionView/types";

interface IVulnRowAttr {
  analyst?: string;
  commitHash: string;
  currentState: "closed" | "open";
  currentStateCapitalized: "Closed" | "Open";
  cycles: string;
  efficacy: string;
  externalBts: string;
  historicTreatment: IHistoricTreatment[];
  id: string;
  lastReattackDate: string;
  lastReattackRequester: string;
  lastRequestedReattackDate: string;
  remediated: boolean;
  reportDate: string;
  severity: string;
  specific: string;
  stream: string;
  tag: string;
  treatment: string;
  treatmentChanges: number;
  treatmentDate: string;
  treatmentManager: string;
  verification: string;
  vulnType: string;
  where: string;
  zeroRisk: string;
}

interface IUploadVulnerabilitiesResultAttr {
  uploadFile: {
    success: boolean;
  };
}

interface IDownloadVulnerabilitiesResultAttr {
  downloadVulnFile: {
    success: boolean;
    url: string;
  };
}

interface IUpdateTreatmentVulnAttr {
  acceptanceDate: string;
  externalBts: string;
  findingId: string;
  justification: string;
  severity?: number;
  tag?: string;
  treatment: string;
  treatmentManager: string;
  vulnerabilities: string[];
}

interface IVulnDataTypeAttr {
  currentState: "closed" | "open";
  externalBts: string;
  historicTreatment: IHistoricTreatment[];
  id: string;
  severity: string;
  specific: string;
  tag: string;
  treatmentManager: string;
  where: string;
}

interface IVulnComponentProps {
  canDisplayAnalyst: boolean;
  findingId: string;
  groupName: string;
  isFindingReleased: boolean;
  isEditing: boolean;
  isRequestingReattack: boolean;
  isVerifyingRequest: boolean;
  vulnerabilities: IVulnRowAttr[];
  onVulnSelect: (
    vulnerabilities: IVulnDataTypeAttr[],
    clearSelected: () => void
  ) => void;
}

export {
  IVulnRowAttr,
  IUploadVulnerabilitiesResultAttr,
  IDownloadVulnerabilitiesResultAttr,
  IUpdateTreatmentVulnAttr,
  IVulnDataTypeAttr,
  IVulnComponentProps,
};
