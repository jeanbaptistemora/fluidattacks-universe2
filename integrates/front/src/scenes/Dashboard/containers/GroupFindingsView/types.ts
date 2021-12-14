interface IGroupFindingsAttr {
  group: {
    findings: IFindingAttr[];
  };
}

interface ITreatmentSummaryAttr {
  accepted: number;
  acceptedUndefined: number;
  inProgress: number;
  new: number;
}

interface IFindingAttr {
  age: number;
  description: string;
  id: string;
  isExploitable: boolean;
  lastVulnerability: number;
  openAge: number;
  openVulnerabilities: number;
  name: string;
  releaseDate: string | null;
  remediated: string;
  severityScore: number;
  state: string;
  title: string;
  treatment: string;
  treatmentSummary: ITreatmentSummaryAttr;
  verified: boolean;
  vulnerabilities?: {
    where: string;
  }[];
  where: string;
}

interface IFindingData {
  age: number;
  description: string;
  id: string;
  isExploitable: boolean;
  lastVulnerability: number;
  openAge: number;
  openVulnerabilities: number;
  name: string;
  releaseDate: string | null;
  remediated: string;
  severityScore: number;
  state: string;
  title: string;
  treatment: string;
  treatmentSummary: ITreatmentSummaryAttr;
  verified: boolean;
  where: string;
}

interface IRequestGroupReportResult {
  requestGroupReport: {
    success: boolean;
  };
}

export {
  IGroupFindingsAttr,
  IFindingAttr,
  IFindingData,
  IRequestGroupReportResult,
  ITreatmentSummaryAttr,
};
