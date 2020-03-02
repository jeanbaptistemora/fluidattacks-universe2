import { IDescriptionViewProps } from "../../containers/DescriptionView";
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
  acceptanceDate: string; btsUrl: string; findingId: string; severity?: string; tag?: string; treatment: string;
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

export interface IVulnerabilitiesViewProps {
  analyst?: boolean;
  descriptParam?: IDescriptionViewProps;
  editMode: boolean;
  editModePending?: boolean;
  findingId: string;
  isRequestVerification?: boolean;
  isVerifyRequest?: boolean;
  renderAsEditable?: boolean;
  separatedRow?: boolean;
  state: string;
  userRole: string;
  vulnerabilities?: IDashboardState["vulnerabilities"];
}

export interface IRequestVerificationVulnResult {
  requestVerificationVuln: { success: boolean };
}
export interface IVerifyRequestVulnResult {
  verifyRequestVuln: { success: boolean };
}

export type IVulnType = (IVulnsAttr["finding"]["pendingVulns"] | IVulnsAttr["finding"]["inputsVulns"] |
IVulnsAttr["finding"]["linesVulns"] | IVulnsAttr["finding"]["portsVulns"]);
