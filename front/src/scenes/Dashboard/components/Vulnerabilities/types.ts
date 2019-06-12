export interface IVulnsAttr {
  finding: {
    id: string;
    inputsVulns: Array<{
      currentState: string; specific: string;
      vulnType: string; where: string;
    }>;
    linesVulns: Array<{
      currentState: string; specific: string;
      vulnType: string; where: string;
    }>;
    portsVulns: Array<{
      currentState: string; specific: string;
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
