/* eslint-disable camelcase */
interface IGroupDraftsAttr {
  group: {
    drafts: {
      currentState: string;
      description: string;
      id: string;
      isExploitable: string;
      openVulnerabilities: number;
      releaseDate: string;
      reportDate: string;
      severityScore: number;
      title: string;
    }[];
    language: string;
    name: string;
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

interface IGroupFindingsStubs {
  group: {
    findings: {
      id: string;
      title: string;
    }[];
  };
}

export {
  IDraftVariables,
  IAddDraftMutationResult,
  IAddDraftMutationVariables,
  IGroupDraftsAttr,
  ISuggestion,
  IRequirementData,
  IVulnData,
  IGroupFindingsStubs,
};
