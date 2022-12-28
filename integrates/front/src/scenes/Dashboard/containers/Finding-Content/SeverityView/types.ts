interface ISeverityAttr {
  finding: {
    cvssVersion: string;
    id: string;
    severity: {
      attackComplexity: string;
      attackVector: string;
      availabilityImpact: string;
      availabilityRequirement: string;
      confidentialityImpact: string;
      confidentialityRequirement: string;
      exploitability: string;
      integrityImpact: string;
      integrityRequirement: string;
      modifiedAttackComplexity: string;
      modifiedAttackVector: string;
      modifiedAvailabilityImpact: string;
      modifiedConfidentialityImpact: string;
      modifiedIntegrityImpact: string;
      modifiedPrivilegesRequired: string;
      modifiedSeverityScope: string;
      modifiedUserInteraction: string;
      privilegesRequired: string;
      remediationLevel: string;
      reportConfidence: string;
      severityScope: string;
      userInteraction: string;
    };
    severityScore: number;
  };
}

interface IUpdateSeverityAttr {
  updateSeverity: {
    finding: {
      cvssVersion: string;
      severity: {
        attackComplexity: string;
        attackVector: string;
        availabilityImpact: string;
        availabilityRequirement: string;
        confidentialityImpact: string;
        confidentialityRequirement: string;
        exploitability: string;
        integrityImpact: string;
        integrityRequirement: string;
        modifiedAttackComplexity: string;
        modifiedAttackVector: string;
        modifiedAvailabilityImpact: string;
        modifiedConfidentialityImpact: string;
        modifiedIntegrityImpact: string;
        modifiedPrivilegesRequired: string;
        modifiedSeverityScope: string;
        modifiedUserInteraction: string;
        privilegesRequired: string;
        remediationLevel: string;
        reportConfidence: string;
        severityScope: string;
        userInteraction: string;
      };
    };
    success: boolean;
  };
}

interface ISeverityField {
  currentValue: string;
  name: string;
  options: Record<string, string>;
  title: string;
  tooltip?: string;
}

export type { ISeverityAttr, IUpdateSeverityAttr, ISeverityField };
