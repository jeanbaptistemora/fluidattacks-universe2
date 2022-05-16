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

interface ILocationsInfoAttr {
  findingId: string;
  openVulnerabilities: number;
  closedVulnerabilities: number;
  locations: string | undefined;
}

interface IFindingAttr {
  age: number;
  closedVulnerabilities: number;
  closingPercentage: number;
  description: string;
  id: string;
  isExploitable: boolean;
  lastVulnerability: number;
  locationsInfo: ILocationsInfoAttr;
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
  ILocationsInfoAttr,
  IRequestGroupReportResult,
  ITreatmentSummaryAttr,
  IVerificationSummaryAttr,
};
