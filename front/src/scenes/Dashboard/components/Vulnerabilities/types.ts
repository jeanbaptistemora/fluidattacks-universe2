import { IDescriptionViewProps } from "../../containers/DescriptionView";

export interface IVulnsAttr {
  finding: {
    id: string;
    inputsVulns: Array<{
      currentState: string; id: string; specific: string; treatment: string;
      vulnType: string; where: string;
    }>;
    linesVulns: Array<{
      currentState: string; id: string; specific: string; treatment: string;
      vulnType: string; where: string;
    }>;
    portsVulns: Array<{
      currentState: string; id: string; specific: string; treatment: string;
      vulnType: string; where: string;
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

export interface IUpdateVulnTreatment {
  updateTreatmentVulnerability: {
    success: boolean;
  };
}

export interface IVulnerabilitiesViewProps {
  descriptParam?: IDescriptionViewProps;
  editMode: boolean;
  findingId: string;
  renderAsEditable?: boolean;
  state: string;
  userRole: string;
}

export type IVulnType = (IVulnsAttr["finding"]["inputsVulns"] | IVulnsAttr["finding"]["linesVulns"] |
IVulnsAttr["finding"]["portsVulns"]);
