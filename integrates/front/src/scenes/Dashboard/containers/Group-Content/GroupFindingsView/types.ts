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
  untreated: number;
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

interface IRoot {
  nickname: string;
  state: "ACTIVE" | "INACTIVE";
}

interface IFindingSuggestionData {
  attackComplexity: number;
  attackVector: number;
  attackVectorDescription: string;
  availabilityImpact: number;
  code: string;
  confidentialityImpact: number;
  description: string;
  exploitability: number;
  integrityImpact: number;
  privilegesRequired: number;
  recommendation: string;
  minTimeToRemediate: number | null;
  remediationLevel: number;
  reportConfidence: number;
  severityScope: number;
  threat: string;
  title: string;
  unfulfilledRequirements: string[];
  userInteraction: number;
}

interface IVulnerabilityLanguage {
  title: string;
  description: string;
  impact: string;
  recommendation: string;
  threat: string;
}

interface IVulnerabilityScore {
  base: {
    attack_vector: string;
    attack_complexity: string;
    privileges_required: string;
    user_interaction: string;
    scope: string;
    confidentiality: string;
    integrity: string;
    availability: string;
  };
  temporal: {
    exploit_code_maturity: string;
    remediation_level: string;
    report_confidence: string;
  };
}

interface IVulnerabilityCriteriaData {
  en: IVulnerabilityLanguage;
  es: IVulnerabilityLanguage;
  score: IVulnerabilityScore;
  remediation_time: string;
  requirements: string[];
  metadata: Record<string, unknown>;
}

interface IAddFindingMutationResult {
  addFinding: {
    success: boolean;
  };
}

export type {
  IAddFindingMutationResult,
  IRoot,
  IGroupFindingsAttr,
  IGroupVulnerabilities,
  IFindingAttr,
  IFindingSuggestionData,
  ILocationsInfoAttr,
  ITreatmentSummaryAttr,
  IVerificationSummaryAttr,
  IVulnerability,
  IVulnerabilitiesResume,
  IVulnerabilityCriteriaData,
};
