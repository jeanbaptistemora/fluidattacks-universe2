import { IHistoricTreatment } from "scenes/Dashboard/containers/DescriptionView/types";

export interface IVulnsAttr {
  finding: {
    id: string;
    inputsVulns: IVulnRow[];
    linesVulns: IVulnRow[];
    portsVulns: IVulnRow[];
    releaseDate: string;
    success: string;
  };
}

export interface IVulnRow {
  analyst: string;
  currentState: string;
  externalBts: string;
  historicTreatment: IHistoricTreatment[];
  id: string;
  remediated: boolean;
  severity: string;
  specific: string;
  tag: string;
  treatment: string;
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
  currentState: string;
  externalBts: string;
  historicTreatment: IHistoricTreatment[];
  id: string;
  severity: string;
  specific: string;
  tag: string;
  treatmentManager: string;
  where: string;
}

export interface IVulnerabilitiesViewProps {
  editMode: boolean;
  findingId: string;
  isConfirmingZeroRisk?: boolean;
  isRejectingZeroRisk?: boolean;
  isRequestVerification?: boolean;
  isVerifyRequest?: boolean;
  projectName?: string;
  separatedRow?: boolean;
  state: "open" | "closed";
  verificationFn?(vulnerabilities: IVulnDataType[], clearSelected: () => void): void;
}

export interface IRequestVerificationVulnResult {
  requestVerificationVuln: { success: boolean };
}
export interface IVerifyRequestVulnResult {
  verifyRequestVuln: { success: boolean };
}

export type IVulnType = (IVulnsAttr["finding"]["inputsVulns"] | IVulnsAttr["finding"]["linesVulns"] |
IVulnsAttr["finding"]["portsVulns"]);
