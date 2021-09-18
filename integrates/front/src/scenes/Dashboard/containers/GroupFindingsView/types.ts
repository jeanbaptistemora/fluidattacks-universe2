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
  lastVulnerabilityReportDate: string;
  oldestOpenVulnerabilityReportDate: string;
  openVulnerabilities: number;
  name: string;
  remediated: string;
  severityScore: number;
  state: string;
  title: string;
  treatment: string;
  treatmentSummary: ITreatmentSummaryAttr;
  verified: boolean;
  where: string;
}

interface IFindingData {
  age: number;
  description: string;
  id: string;
  isExploitable: boolean;
  lastReport: number;
  lastVulnerability: number;
  lastVulnerabilityReportDate: string;
  oldestOpenVulnerabilityReportDate: string;
  openAge: number;
  openVulnerabilities: number;
  name: string;
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
