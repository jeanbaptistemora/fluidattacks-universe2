import { translate } from "utils/translations/translate";
import type {
  ISeverityAttr,
  ISeverityField,
} from "scenes/Dashboard/containers/SeverityView/types";

const castPrivileges: (scope: string) => Record<string, string> = (
  scope: string
): Record<string, string> => {
  const privilegesRequiredScope: Record<string, string> = {
    0.5: "search_findings.tab_severity.privilegesRequiredOptions.high.text",
    0.68: "search_findings.tab_severity.privilegesRequiredOptions.low.text",
    0.85: "search_findings.tab_severity.privilegesRequiredOptions.none.text",
  };
  const privilegesRequiredNoScope: Record<string, string> = {
    0.27: "search_findings.tab_severity.privilegesRequiredOptions.high.text",
    0.62: "search_findings.tab_severity.privilegesRequiredOptions.low.text",
    0.85: "search_findings.tab_severity.privilegesRequiredOptions.none.text",
  };
  const privilegesOptions: Record<string, string> =
    parseInt(scope, 10) === 1
      ? privilegesRequiredScope
      : privilegesRequiredNoScope;

  return privilegesOptions;
};

/**
 * Values were taken from:
 * @see https://www.first.org/cvss/specification-document#7-4-Metric-Values
 */
export const castFieldsCVSS3: (
  dataset: ISeverityAttr["finding"]["severity"],
  isEditing: boolean,
  formValues: Record<string, string>
) => ISeverityField[] = (
  dataset: ISeverityAttr["finding"]["severity"],
  isEditing: boolean,
  formValues: Record<string, string>
): ISeverityField[] => {
  const attackVector: Record<string, string> = {
    0.2: "search_findings.tab_severity.attackVectorOptions.physical.text",
    0.55: "search_findings.tab_severity.attackVectorOptions.local.text",
    0.62: "search_findings.tab_severity.attackVectorOptions.adjacent.text",
    0.85: "search_findings.tab_severity.attackVectorOptions.network.text",
  };

  const attackComplexity: Record<string, string> = {
    0.44: "search_findings.tab_severity.attackComplexityOptions.high.text",
    0.77: "search_findings.tab_severity.attackComplexityOptions.low.text",
  };

  const userInteraction: Record<string, string> = {
    0.62: "search_findings.tab_severity.userInteractionOptions.required.text",
    0.85: "search_findings.tab_severity.userInteractionOptions.none.text",
  };

  const severityScope: Record<string, string> = {
    0: "search_findings.tab_severity.severityScopeOptions.unchanged.text",
    1: "search_findings.tab_severity.severityScopeOptions.changed.text",
  };

  const confidentialityImpact: Record<string, string> = {
    0: "search_findings.tab_severity.confidentialityImpactOptions.none.text",
    0.22: "search_findings.tab_severity.confidentialityImpactOptions.low.text",
    0.56: "search_findings.tab_severity.confidentialityImpactOptions.high.text",
  };

  const integrityImpact: Record<string, string> = {
    0: "search_findings.tab_severity.integrityImpactOptions.none.text",
    0.22: "search_findings.tab_severity.integrityImpactOptions.low.text",
    0.56: "search_findings.tab_severity.integrityImpactOptions.high.text",
  };

  const availabilityImpact: Record<string, string> = {
    0: "search_findings.tab_severity.availabilityImpactOptions.none.text",
    0.22: "search_findings.tab_severity.availabilityImpactOptions.low.text",
    0.56: "search_findings.tab_severity.availabilityImpactOptions.high.text",
  };

  const exploitability: Record<string, string> = {
    0.91: "search_findings.tab_severity.exploitabilityOptions.unproven.text",
    0.94: "search_findings.tab_severity.exploitabilityOptions.proofOfConcept.text",
    0.97: "search_findings.tab_severity.exploitabilityOptions.functional.text",
    1: "search_findings.tab_severity.exploitabilityOptions.high.text",
  };

  const remediationLevel: Record<string, string> = {
    0.95: "search_findings.tab_severity.remediationLevelOptions.officialFix.text",
    0.96: "search_findings.tab_severity.remediationLevelOptions.temporaryFix.text",
    0.97: "search_findings.tab_severity.remediationLevelOptions.workaround.text",
    1: "search_findings.tab_severity.remediationLevelOptions.unavailable.text",
  };

  const reportConfidence: Record<string, string> = {
    0.92: "search_findings.tab_severity.reportConfidenceOptions.unknown.text",
    0.96: "search_findings.tab_severity.reportConfidenceOptions.reasonable.text",
    1: "search_findings.tab_severity.reportConfidenceOptions.confirmed.text",
  };

  const fields: ISeverityField[] = [
    {
      currentValue: dataset.attackVector,
      name: "attackVector",
      options: attackVector,
      title: translate.t("search_findings.tab_severity.attackVector"),
    },
    {
      currentValue: dataset.attackComplexity,
      name: "attackComplexity",
      options: attackComplexity,
      title: translate.t("search_findings.tab_severity.attackComplexity"),
    },
    {
      currentValue: dataset.userInteraction,
      name: "userInteraction",
      options: userInteraction,
      title: translate.t("search_findings.tab_severity.userInteraction"),
    },
    {
      currentValue: dataset.severityScope,
      name: "severityScope",
      options: severityScope,
      title: translate.t("search_findings.tab_severity.severityScope"),
    },
    {
      currentValue: dataset.confidentialityImpact,
      name: "confidentialityImpact",
      options: confidentialityImpact,
      title: translate.t("search_findings.tab_severity.confidentialityImpact"),
    },
    {
      currentValue: dataset.integrityImpact,
      name: "integrityImpact",
      options: integrityImpact,
      title: translate.t("search_findings.tab_severity.integrityImpact"),
    },
    {
      currentValue: dataset.availabilityImpact,
      name: "availabilityImpact",
      options: availabilityImpact,
      title: translate.t("search_findings.tab_severity.availabilityImpact"),
    },
    {
      currentValue: dataset.exploitability,
      name: "exploitability",
      options: exploitability,
      title: translate.t("search_findings.tab_severity.exploitability"),
    },
    {
      currentValue: dataset.remediationLevel,
      name: "remediationLevel",
      options: remediationLevel,
      title: translate.t("search_findings.tab_severity.remediationLevel"),
    },
    {
      currentValue: dataset.reportConfidence,
      name: "reportConfidence",
      options: reportConfidence,
      title: translate.t("search_findings.tab_severity.reportConfidence"),
    },
    {
      currentValue: dataset.privilegesRequired,
      name: "privilegesRequired",
      options: castPrivileges(formValues.severityScope),
      title: translate.t("search_findings.tab_severity.privilegesRequired"),
    },
  ];

  const confidentialityRequirement: Record<string, string> = {
    0.5: "search_findings.tab_severity.confidentialityRequirementOptions.low.text",
    1: "search_findings.tab_severity.confidentialityRequirementOptions.medium.text",
    1.5: "search_findings.tab_severity.confidentialityRequirementOptions.high.text",
  };

  const integrityRequirement: Record<string, string> = {
    0.5: "search_findings.tab_severity.integrityRequirementOptions.low.text",
    1: "search_findings.tab_severity.integrityRequirementOptions.medium.text",
    1.5: "search_findings.tab_severity.integrityRequirementOptions.high.text",
  };

  const availabilityRequirement: Record<string, string> = {
    0.5: "search_findings.tab_severity.availabilityRequirementOptions.low.text",
    1: "search_findings.tab_severity.availabilityRequirementOptions.medium.text",
    1.5: "search_findings.tab_severity.availabilityRequirementOptions.high.text",
  };

  const environmentFields: ISeverityField[] = [
    {
      currentValue: dataset.confidentialityRequirement,
      name: "confidentialityRequirement",
      options: confidentialityRequirement,
      title: translate.t(
        "search_findings.tab_severity.confidentialityRequirement"
      ),
    },
    {
      currentValue: dataset.integrityRequirement,
      name: "integrityRequirement",
      options: integrityRequirement,
      title: translate.t("search_findings.tab_severity.integrityRequirement"),
    },
    {
      currentValue: dataset.availabilityRequirement,
      name: "availabilityRequirement",
      options: availabilityRequirement,
      title: translate.t(
        "search_findings.tab_severity.availabilityRequirement"
      ),
    },
    {
      currentValue: dataset.modifiedAttackVector,
      name: "modifiedAttackVector",
      options: attackVector,
      title: translate.t("search_findings.tab_severity.modifiedAttackVector"),
    },
    {
      currentValue: dataset.modifiedAttackComplexity,
      name: "modifiedAttackComplexity",
      options: attackComplexity,
      title: translate.t(
        "search_findings.tab_severity.modifiedAttackComplexity"
      ),
    },
    {
      currentValue: dataset.modifiedUserInteraction,
      name: "modifiedUserInteraction",
      options: userInteraction,
      title: translate.t(
        "search_findings.tab_severity.modifiedUserInteraction"
      ),
    },
    {
      currentValue: dataset.modifiedSeverityScope,
      name: "modifiedSeverityScope",
      options: severityScope,
      title: translate.t("search_findings.tab_severity.modifiedSeverityScope"),
    },
    {
      currentValue: dataset.modifiedConfidentialityImpact,
      name: "modifiedConfidentialityImpact",
      options: confidentialityImpact,
      title: translate.t(
        "search_findings.tab_severity.modifiedConfidentialityImpact"
      ),
    },
    {
      currentValue: dataset.modifiedIntegrityImpact,
      name: "modifiedIntegrityImpact",
      options: integrityImpact,
      title: translate.t(
        "search_findings.tab_severity.modifiedIntegrityImpact"
      ),
    },
    {
      currentValue: dataset.modifiedAvailabilityImpact,
      name: "modifiedAvailabilityImpact",
      options: availabilityImpact,
      title: translate.t(
        "search_findings.tab_severity.modifiedAvailabilityImpact"
      ),
    },
  ];

  if (isEditing && formValues.cvssVersion === "3.1") {
    return [
      ...fields,
      ...environmentFields,
      {
        currentValue: dataset.modifiedPrivilegesRequired,
        name: "modifiedPrivilegesRequired",
        options: castPrivileges(formValues.modifiedSeverityScope),
        title: translate.t(
          "search_findings.tab_severity.modifiedPrivilegesRequired"
        ),
      },
    ];
  }

  return fields;
};
