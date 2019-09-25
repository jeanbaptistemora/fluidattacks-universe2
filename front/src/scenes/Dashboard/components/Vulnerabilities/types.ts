import { IDescriptionViewProps } from "../../containers/DescriptionView";

export interface IVulnsAttr {
  finding: {
    id: string;
    inputsVulns: Array<{
      analyst: string; currentApprovalStatus: string; currentState: string; externalBts: string; id: string;
      isNew: string; lastAnalyst: string; lastApprovedStatus: string; specific: string; treatment: string;
      treatmentJustification: string; treatmentManager: string; vulnType: string; where: string;
    }>;
    linesVulns: Array<{
      analyst: string; currentApprovalStatus: string; currentState: string; externalBts: string; id: string;
      isNew: string; lastAnalyst: string; lastApprovedStatus: string; specific: string; treatment: string;
      treatmentJustification: string; treatmentManager: string; vulnType: string; where: string;
    }>;
    pendingVulns: Array<{
      analyst: string; currentApprovalStatus: string; currentState: string; externalBts: string; id: string;
      isNew: string; lastAnalyst: string; lastApprovedStatus: string; specific: string; treatment: string;
      treatmentJustification: string; treatmentManager: string; vulnType: string; where: string;
    }>;
    portsVulns: Array<{
      analyst: string; currentApprovalStatus: string; currentState: string; externalBts: string; id: string;
      isNew: string; lastAnalyst: string; lastApprovedStatus: string; specific: string; treatment: string;
      treatmentJustification: string; treatmentManager: string; vulnType: string; where: string;
    }>;
    releaseDate: string;
    success: string;
  };
}

export interface IDeleteVulnAttr {
  deleteVulnerability: {
    success: boolean;
  };
}

export interface IApproveVulnAttr {
  approveVulnerability: {
    success: boolean;
  };
}

export interface IUpdateVulnTreatment {
  updateTreatmentVuln: {
    success: boolean;
  };
}

export interface IVulnerabilitiesViewProps {
  analyst?: boolean;
  descriptParam?: IDescriptionViewProps;
  editMode: boolean;
  editModePending?: boolean;
  findingId: string;
  renderAsEditable?: boolean;
  separatedRow?: boolean;
  state: string;
  userRole: string;
}

export type IVulnType = (IVulnsAttr["finding"]["pendingVulns"] | IVulnsAttr["finding"]["inputsVulns"] |
IVulnsAttr["finding"]["linesVulns"] | IVulnsAttr["finding"]["portsVulns"]);
