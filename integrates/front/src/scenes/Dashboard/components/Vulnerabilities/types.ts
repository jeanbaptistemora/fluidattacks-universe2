import { IHistoricTreatment } from "scenes/Dashboard/containers/DescriptionView/types";

export interface IVulnRowAttr {
  currentState: "open" | "closed";
  currentStateCapitalized: "Open" | "Closed";
  cycles: string;
  efficacy: string;
  externalBts: string;
  historicTreatment: IHistoricTreatment[];
  id: string;
  lastRequestedReattackDate: string;
  remediated: boolean;
  reportDate: string;
  severity: string;
  specific: string;
  tag: string;
  treatment: string;
  treatmentDate: string;
  treatmentManager: string;
  verification: string;
  vulnType: string;
  where: string;
  zeroRisk: string;
}

export interface IUploadVulnerabilitiesResult {
  uploadFile: {
    success: boolean;
  };
}

export interface IDownloadVulnerabilitiesResult {
  downloadVulnFile: {
    success: boolean;
    url: string;
  };
}

export interface IUpdateTreatmentVulnAttr {
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

export interface IVulnDataType {
  currentState: "open" | "closed";
  externalBts: string;
  historicTreatment: IHistoricTreatment[];
  id: string;
  severity: string;
  specific: string;
  tag: string;
  treatmentManager: string;
  where: string;
}

export interface IVulnComponentProps {
  findingId: string;
  groupName: string;
  isEditing: boolean;
  isRequestingReattack: boolean;
  isVerifyingRequest: boolean;
  vulnerabilities: IVulnRowAttr[];
  onVulnSelect(vulnerabilities: IVulnDataType[], clearSelected: () => void): void;
}

export interface IRequestVerificationVulnResult {
  requestVerificationVuln: { success: boolean };
}
export interface IVerifyRequestVulnResult {
  verifyRequestVuln: { success: boolean };
}
