interface IGroupFindingsAttr {
  group: {
    findings: IFindingAttr[];
    businessId: string;
    businessName: string;
    description: string;
    hasMachine: boolean;
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
  treatmentAssignmentEmails: Set<string>;
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
  status: "SAFE" | "VULNERABLE";
  title: string;
  treatment: string;
  treatmentSummary: ITreatmentSummaryAttr;
  verificationSummary: IVerificationSummaryAttr;
  verified: boolean;
}

interface IVulnerability {
  findingId: string;
  id: string;
  state: string;
  treatmentAssigned: string | null;
  where: string;
}

interface IGroupVulnerabilities {
  group: {
    name: string;
    vulnerabilities: {
      edges: { node: IVulnerability }[];
      pageInfo: {
        endCursor: string;
        hasNextPage: boolean;
      };
    };
  };
}

interface IVulnerabilitiesResume {
  treatmentAssignmentEmails: Set<string>;
  wheres: string;
}

export type {
  IGroupFindingsAttr,
  IGroupVulnerabilities,
  IFindingAttr,
  ILocationsInfoAttr,
  ITreatmentSummaryAttr,
  IVerificationSummaryAttr,
  IVulnerability,
  IVulnerabilitiesResume,
};
