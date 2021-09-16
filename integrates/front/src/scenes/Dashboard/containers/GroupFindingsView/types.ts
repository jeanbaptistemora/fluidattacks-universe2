interface IGroupFindingsAttr {
  group: {
    findings: IFindingAttr[];
  };
}

interface IFindingAttr {
  age: number;
  description: string;
  id: string;
  isExploitable: string;
  lastVulnerability: number;
  openVulnerabilities: number;
  name: string;
  remediated: string;
  severityScore: number;
  state: string;
  title: string;
  treatment: string;
  treatmentSummary: {
    accepted: number;
    acceptedUndefined: number;
    inProgress: number;
    new: number;
  };
  verified: boolean;
  where: string;
}

interface IRequestGroupReportResult {
  requestGroupReport: {
    success: boolean;
  };
}

export { IGroupFindingsAttr, IFindingAttr, IRequestGroupReportResult };
