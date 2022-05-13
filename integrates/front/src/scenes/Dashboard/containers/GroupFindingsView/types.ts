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

interface IVerificationSummaryAttr {
  onHold: number;
  requested: number;
  verified: number;
}

interface IFindingAttr {
  age: number;
  closedVulnerabilities: number;
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
  reattack: string;
  releaseDate: string | null;
  severityScore: number;
  state: string;
  title: string;
  treatment: string;
  treatmentSummary: ITreatmentSummaryAttr;
  verificationSummary: IVerificationSummaryAttr;
  verified: boolean;
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
  severityScore: number;
  state: string;
  title: string;
  treatment: string;
  treatmentSummary: ITreatmentSummaryAttr;
  verificationSummary: IVerificationSummaryAttr;
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
  IVerificationSummaryAttr,
};
