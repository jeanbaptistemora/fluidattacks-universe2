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
      type: string;
    }[];
    language: string;
    name: string;
  };
}

interface ISuggestion {
  attackComplexity: string;
  attackVector: string;
  attackVectorDesc: string;
  availabilityImpact: string;
  confidentialityImpact: string;
  cwe: string;
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

export { IGroupDraftsAttr, ISuggestion, IVulnData };
