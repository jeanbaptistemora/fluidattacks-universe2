import { IHistoricTreatment } from "scenes/Dashboard/containers/DescriptionView/types";

export interface IVulnsAttr {
  finding: {
    btsUrl?: string;
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
  id: string;
  remediated: boolean;
  severity: string;
  specific: string;
  tag: string;
  treatmentManager: string;
  verification: string;
  vulnType: string;
  where: string;
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
  findingId: string;
  severity?: number;
  tag?: string;
  treatmentManager: string;
  vulnerabilities: string[];
}

export interface IUpdateVulnTreatment {
  updateTreatmentVuln: {
    success: boolean;
  };
}

export interface IDeleteTagResult {
  deleteTags: {
    success: boolean;
  };
}

export interface IDeleteTagAttr {
  findingId: string;
  tag?: string;
  vulnerabilities: string[];
}

export interface IVulnDataType {
  currentState: string;
  id: string;
  specific: string;
  treatments: {
    severity: string;
    tag: string;
    treatmentManager: string;
  };
  where: string;
}

export interface IVulnerabilitiesViewProps {
  btsUrl?: string;
  editMode: boolean;
  editModePending?: boolean;
  findingId: string;
  isRequestVerification?: boolean;
  isVerifyRequest?: boolean;
  lastTreatment?: IHistoricTreatment;
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
