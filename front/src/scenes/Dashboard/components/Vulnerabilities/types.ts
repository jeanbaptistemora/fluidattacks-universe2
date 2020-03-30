import { IHistoricTreatment } from "../../containers/DescriptionView/types";
import { IDashboardState } from "../../reducer";

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
  acceptanceDate: string; analyst: string; currentApprovalStatus: string; currentState: string; externalBts: string;
  id: string; isNew: string; lastAnalyst: string; lastApprovedStatus: string; remediated: boolean; severity: string;
  specific: string; tag: string; treatment: string; treatmentJustification: string; treatmentManager: string;
  verification: string; vulnType: string; where: string;
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
  acceptanceDate: string; btsUrl: string; findingId: string; severity?: number; tag?: string; treatment: string;
  treatmentJustification: string; treatmentManager: string; vulnerabilities: string[];
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
    acceptanceDate: string;
    btsUrl: string;
    severity: string;
    tag: string;
    treatment: string;
    treatmentJustification: string;
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
  vulnerabilities?: IDashboardState["vulnerabilities"];
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
