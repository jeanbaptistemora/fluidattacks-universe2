import { IHistoricTreatment } from "../../containers/DescriptionView/types";

export interface IVulnsAttr {
  finding: {
    id: string;
    inputsVulns: IVulnRow[];
    linesVulns: IVulnRow[];
    pendingVulns: IVulnRow[];
    portsVulns: IVulnRow[];
    releaseDate: string;
    success: string;
  };
}

export interface IVulnRow {
  analyst: string;
  currentApprovalStatus: string;
  currentState: string;
  id: string;
  isNew: string;
  lastAnalyst: string;
  lastApprovedStatus: string;
  remediated: boolean;
  severity: string;
  specific: string;
  tag: string;
  treatmentManager: string;
  verification: string;
  vulnType: string;
  where: string;
}

export interface IApproveVulnAttr {
  approveVulnerability: {
    success: boolean;
  };
}

export interface IUploadVulnerabilitiesResult {
  uploadFile: {
    success: boolean;
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
  findingId: string; vulnerabilities: string[];
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
  analyst?: boolean;
  btsUrl?: string;
  editMode: boolean;
  editModePending?: boolean;
  findingId: string;
  isRequestVerification?: boolean;
  isVerifyRequest?: boolean;
  lastTreatment?: IHistoricTreatment;
  projectName?: string;
  separatedRow?: boolean;
  state: string;
  userRole: string;
  verificationFn?(vulnerabilities: IVulnDataType[], action: "request" | "verify", clearSelected: () => void): void;
}

export interface IRequestVerificationVulnResult {
  requestVerificationVuln: { success: boolean };
}
export interface IVerifyRequestVulnResult {
  verifyRequestVuln: { success: boolean };
}

export type IVulnType = (IVulnsAttr["finding"]["pendingVulns"] | IVulnsAttr["finding"]["inputsVulns"] |
IVulnsAttr["finding"]["linesVulns"] | IVulnsAttr["finding"]["portsVulns"]);
