interface IGroupFindingsAttr {
  group: {
    findings: IFindingAttr[];
    businessId: string;
    businessName: string;
    description: string;
    userRole: string;
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
  closingPercentage: number;
  description: string;
  id: string;
  isExploitable: boolean;
  lastVulnerability: number;
  locationsFindingId: string;
  openAge: number;
  openVulnerabilities: number;
  minTimeToRemediate: number | null;
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
    currentState: string;
    id: string;
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

export type {
  IGroupFindingsAttr,
  IFindingAttr,
  IFindingData,
  IRequestGroupReportResult,
  ITreatmentSummaryAttr,
};
