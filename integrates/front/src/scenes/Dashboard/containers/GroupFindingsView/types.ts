/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

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

interface IVulnerability {
  currentState: "closed" | "open";
  findingId: string;
  id: string;
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
  IFindingData,
  ILocationsInfoAttr,
  IRequestGroupReportResult,
  ITreatmentSummaryAttr,
  IVerificationSummaryAttr,
  IVulnerability,
  IVulnerabilitiesResume,
};
