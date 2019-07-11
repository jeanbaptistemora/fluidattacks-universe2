export interface IVulnsAttr {
  finding: {
    id: string;
    inputsVulns: Array<{
      currentState: string; specific: string; treatment: string;
      vulnType: string; where: string;
    }>;
    linesVulns: Array<{
      currentState: string; specific: string; treatment: string;
      vulnType: string; where: string;
    }>;
    portsVulns: Array<{
      currentState: string; specific: string; treatment: string;
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

export interface IVulnerabilitiesViewProps {
  editMode: boolean;
  findingId: string;
  state: string;
  userRole: string;
}

export type IVulnType = (IVulnsAttr["finding"]["inputsVulns"] | IVulnsAttr["finding"]["linesVulns"] |
IVulnsAttr["finding"]["portsVulns"]);
