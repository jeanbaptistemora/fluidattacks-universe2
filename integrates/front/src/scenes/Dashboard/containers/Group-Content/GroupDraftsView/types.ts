/* eslint-disable camelcase */
interface IGroupDraftsAndFindingsAttr {
  group: {
    drafts: {
      currentState: string;
      description: string;
      id: string;
      isExploitable: string;
      openVulnerabilities: number;
      releaseDate: string | null;
      reportDate: string | null;
      severityScore: number;
      title: string;
    }[];
    findings: {
      title: string;
    }[];
    language: string;
    name: string;
  };
}
interface IGetMeHasDraftsRejected {
  me: {
    hasDraftsRejected: boolean;
    userEmail: string;
  };
}

interface IDraftVariables {
  attackComplexity: string;
  attackVector: string;
  attackVectorDescription: string;
  availabilityImpact: string;
  confidentialityImpact: string;
  description: string;
  exploitability: string;
  integrityImpact: string;
  privilegesRequired: string;
  recommendation: string;
  minTimeToRemediate: string | null;
  remediationLevel: string;
  reportConfidence: string;
  requirements: string;
  severityScope: string;
  threat: string;
  title: string;
  userInteraction: string;
}

interface IAddDraftMutationVariables extends IDraftVariables {
  groupName: string;
}

interface IAddDraftMutationResult {
  addDraft: {
    success: boolean;
  };
}

interface ISuggestion extends IDraftVariables {
  key: string;
}

interface IVulnLanguage {
  title: string;
  description: string;
  impact: string;
  recommendation: string;
  threat: string;
}

interface IVulnScore {
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

interface IVulnData {
  en: IVulnLanguage;
  es: IVulnLanguage;
  score: IVulnScore;
  remediation_time: string;
  requirements: string[];
  metadata: Record<string, unknown>;
}

interface IRequirementLanguage {
  title: string;
  summary: string;
  description: string;
}

interface IRequirementData {
  en: IRequirementLanguage;
  es: IRequirementLanguage;
  category: string;
  references: string;
  metadata: Record<string, unknown>;
}

export type {
  IDraftVariables,
  IAddDraftMutationResult,
  IAddDraftMutationVariables,
  IGetMeHasDraftsRejected,
  IGroupDraftsAndFindingsAttr,
  ISuggestion,
  IRequirementData,
  IVulnData,
};
