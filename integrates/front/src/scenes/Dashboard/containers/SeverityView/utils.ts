import { translate } from "utils/translations/translate";
import type {
  ISeverityAttr,
  ISeverityField,
} from "scenes/Dashboard/containers/SeverityView/types";

const castPrivileges: (scope: string) => Record<string, string> = (
  scope: string
): Record<string, string> => {
  const privilegesRequiredScope: Record<string, string> = {
    0.5: "searchFindings.tabSeverity.privilegesRequiredOptions.high.text",
    0.68: "searchFindings.tabSeverity.privilegesRequiredOptions.low.text",
    0.85: "searchFindings.tabSeverity.privilegesRequiredOptions.none.text",
  };
  const privilegesRequiredNoScope: Record<string, string> = {
    0.27: "searchFindings.tabSeverity.privilegesRequiredOptions.high.text",
    0.62: "searchFindings.tabSeverity.privilegesRequiredOptions.low.text",
    0.85: "searchFindings.tabSeverity.privilegesRequiredOptions.none.text",
  };
  const privilegesOptions: Record<string, string> =
    parseInt(scope, 10) === 1
      ? privilegesRequiredScope
      : privilegesRequiredNoScope;

  return privilegesOptions;
};

const attackComplexityBgColor: Record<string, string> = {
  0.44: "bg-lbl-yellow",
  0.77: "bg-dark-red",
};

const attackComplexityOptions: Record<string, string> = {
  0.44: "searchFindings.tabSeverity.attackComplexityOptions.high.text",
  0.77: "searchFindings.tabSeverity.attackComplexityOptions.low.text",
};

const attackVectorBgColor: Record<string, string> = {
  0.2: "bg-lbl-yellow",
  0.55: "bg-orange",
  0.62: "bg-red",
  0.85: "bg-dark-red",
};

const attackVectorOptions: Record<string, string> = {
  0.2: "searchFindings.tabSeverity.attackVectorOptions.physical.text",
  0.55: "searchFindings.tabSeverity.attackVectorOptions.local.text",
  0.62: "searchFindings.tabSeverity.attackVectorOptions.adjacent.text",
  0.85: "searchFindings.tabSeverity.attackVectorOptions.network.text",
};

const availabilityImpactBgColor: Record<string, string> = {
  0: "bg-lbl-green",
  0.22: "bg-lbl-yellow",
  0.56: "bg-dark-red",
};

const availabilityImpactOptions: Record<string, string> = {
  0: "searchFindings.tabSeverity.availabilityImpactOptions.none.text",
  0.22: "searchFindings.tabSeverity.availabilityImpactOptions.low.text",
  0.56: "searchFindings.tabSeverity.availabilityImpactOptions.high.text",
};

const confidentialityImpactBgColor: Record<string, string> = {
  0: "bg-lbl-green",
  0.22: "bg-lbl-yellow",
  0.56: "bg-dark-red",
};

const confidentialityImpactOptions: Record<string, string> = {
  0: "searchFindings.tabSeverity.confidentialityImpactOptions.none.text",
  0.22: "searchFindings.tabSeverity.confidentialityImpactOptions.low.text",
  0.56: "searchFindings.tabSeverity.confidentialityImpactOptions.high.text",
};

const exploitabilityBgColor: Record<string, string> = {
  0.91: "bg-lbl-yellow",
  0.94: "bg-orange",
  0.97: "bg-red",
  1: "bg-dark-red",
};

const exploitabilityOptions: Record<string, string> = {
  0.91: "searchFindings.tabSeverity.exploitabilityOptions.unproven.text",
  0.94: "searchFindings.tabSeverity.exploitabilityOptions.proofOfConcept.text",
  0.97: "searchFindings.tabSeverity.exploitabilityOptions.functional.text",
  1: "searchFindings.tabSeverity.exploitabilityOptions.high.text",
};

const integrityImpactBgColor: Record<string, string> = {
  0: "bg-lbl-green",
  0.22: "bg-lbl-yellow",
  0.56: "bg-dark-red",
};

const integrityImpactOptions: Record<string, string> = {
  0: "searchFindings.tabSeverity.integrityImpactOptions.none.text",
  0.22: "searchFindings.tabSeverity.integrityImpactOptions.low.text",
  0.56: "searchFindings.tabSeverity.integrityImpactOptions.high.text",
};

const remediationLevelBgColor: Record<string, string> = {
  0.95: "bg-lbl-green",
  0.96: "bg-lbl-yellow",
  0.97: "bg-orange",
  1: "bg-dark-red",
};

const remediationLevelOptions: Record<string, string> = {
  0.95: "searchFindings.tabSeverity.remediationLevelOptions.officialFix.text",
  0.96: "searchFindings.tabSeverity.remediationLevelOptions.temporaryFix.text",
  0.97: "searchFindings.tabSeverity.remediationLevelOptions.workaround.text",
  1: "searchFindings.tabSeverity.remediationLevelOptions.unavailable.text",
};

const reportConfidenceBgColor: Record<string, string> = {
  0.92: "bg-lbl-yellow",
  0.96: "bg-orange",
  1: "bg-dark-red",
};

const reportConfidenceOptions: Record<string, string> = {
  0.92: "searchFindings.tabSeverity.reportConfidenceOptions.unknown.text",
  0.96: "searchFindings.tabSeverity.reportConfidenceOptions.reasonable.text",
  1: "searchFindings.tabSeverity.reportConfidenceOptions.confirmed.text",
};

const severityScopeBgColor: Record<string, string> = {
  0: "bg-lbl-yellow",
  1: "bg-dark-red",
};

const severityScopeOptions: Record<string, string> = {
  0: "searchFindings.tabSeverity.severityScopeOptions.unchanged.text",
  1: "searchFindings.tabSeverity.severityScopeOptions.changed.text",
};

const userInteractionBgColor: Record<string, string> = {
  0.62: "bg-lbl-yellow",
  0.85: "bg-dark-red",
};

const userInteractionOptions: Record<string, string> = {
  0.62: "searchFindings.tabSeverity.userInteractionOptions.required.text",
  0.85: "searchFindings.tabSeverity.userInteractionOptions.none.text",
};

/**
 * Values were taken from:
 * @see https://www.first.org/cvss/specification-document#7-4-Metric-Values
 */
const castFieldsCVSS3: (
  dataset: ISeverityAttr["finding"]["severity"],
  isEditing: boolean,
  formValues: Record<string, string>
) => ISeverityField[] = (
  dataset: ISeverityAttr["finding"]["severity"],
  isEditing: boolean,
  formValues: Record<string, string>
): ISeverityField[] => {
  const fields: ISeverityField[] = [
    {
      currentValue: dataset.attackVector,
      name: "attackVector",
      options: attackVectorOptions,
      title: translate.t("searchFindings.tabSeverity.attackVector"),
    },
    {
      currentValue: dataset.attackComplexity,
      name: "attackComplexity",
      options: attackComplexityOptions,
      title: translate.t("searchFindings.tabSeverity.attackComplexity"),
    },
    {
      currentValue: dataset.userInteraction,
      name: "userInteraction",
      options: userInteractionOptions,
      title: translate.t("searchFindings.tabSeverity.userInteraction"),
    },
    {
      currentValue: dataset.severityScope,
      name: "severityScope",
      options: severityScopeOptions,
      title: translate.t("searchFindings.tabSeverity.severityScope"),
    },
    {
      currentValue: dataset.confidentialityImpact,
      name: "confidentialityImpact",
      options: confidentialityImpactOptions,
      title: translate.t("searchFindings.tabSeverity.confidentialityImpact"),
    },
    {
      currentValue: dataset.integrityImpact,
      name: "integrityImpact",
      options: integrityImpactOptions,
      title: translate.t("searchFindings.tabSeverity.integrityImpact"),
    },
    {
      currentValue: dataset.availabilityImpact,
      name: "availabilityImpact",
      options: availabilityImpactOptions,
      title: translate.t("searchFindings.tabSeverity.availabilityImpact"),
    },
    {
      currentValue: dataset.exploitability,
      name: "exploitability",
      options: exploitabilityOptions,
      title: translate.t("searchFindings.tabSeverity.exploitability"),
    },
    {
      currentValue: dataset.remediationLevel,
      name: "remediationLevel",
      options: remediationLevelOptions,
      title: translate.t("searchFindings.tabSeverity.remediationLevel"),
    },
    {
      currentValue: dataset.reportConfidence,
      name: "reportConfidence",
      options: reportConfidenceOptions,
      title: translate.t("searchFindings.tabSeverity.reportConfidence"),
    },
    {
      currentValue: dataset.privilegesRequired,
      name: "privilegesRequired",
      options: castPrivileges(formValues.severityScope),
      title: translate.t("searchFindings.tabSeverity.privilegesRequired"),
    },
  ];

  const confidentialityRequirement: Record<string, string> = {
    0.5: "searchFindings.tabSeverity.confidentialityRequirementOptions.low.text",
    1: "searchFindings.tabSeverity.confidentialityRequirementOptions.medium.text",
    1.5: "searchFindings.tabSeverity.confidentialityRequirementOptions.high.text",
  };

  const integrityRequirement: Record<string, string> = {
    0.5: "searchFindings.tabSeverity.integrityRequirementOptions.low.text",
    1: "searchFindings.tabSeverity.integrityRequirementOptions.medium.text",
    1.5: "searchFindings.tabSeverity.integrityRequirementOptions.high.text",
  };

  const availabilityRequirement: Record<string, string> = {
    0.5: "searchFindings.tabSeverity.availabilityRequirementOptions.low.text",
    1: "searchFindings.tabSeverity.availabilityRequirementOptions.medium.text",
    1.5: "searchFindings.tabSeverity.availabilityRequirementOptions.high.text",
  };

  const environmentFields: ISeverityField[] = [
    {
      currentValue: dataset.confidentialityRequirement,
      name: "confidentialityRequirement",
      options: confidentialityRequirement,
      title: translate.t(
        "searchFindings.tabSeverity.confidentialityRequirement"
      ),
    },
    {
      currentValue: dataset.integrityRequirement,
      name: "integrityRequirement",
      options: integrityRequirement,
      title: translate.t("searchFindings.tabSeverity.integrityRequirement"),
    },
    {
      currentValue: dataset.availabilityRequirement,
      name: "availabilityRequirement",
      options: availabilityRequirement,
      title: translate.t("searchFindings.tabSeverity.availabilityRequirement"),
    },
    {
      currentValue: dataset.modifiedAttackVector,
      name: "modifiedAttackVector",
      options: attackVectorOptions,
      title: translate.t("searchFindings.tabSeverity.modifiedAttackVector"),
    },
    {
      currentValue: dataset.modifiedAttackComplexity,
      name: "modifiedAttackComplexity",
      options: attackComplexityOptions,
      title: translate.t("searchFindings.tabSeverity.modifiedAttackComplexity"),
    },
    {
      currentValue: dataset.modifiedUserInteraction,
      name: "modifiedUserInteraction",
      options: userInteractionOptions,
      title: translate.t("searchFindings.tabSeverity.modifiedUserInteraction"),
    },
    {
      currentValue: dataset.modifiedSeverityScope,
      name: "modifiedSeverityScope",
      options: severityScopeOptions,
      title: translate.t("searchFindings.tabSeverity.modifiedSeverityScope"),
    },
    {
      currentValue: dataset.modifiedConfidentialityImpact,
      name: "modifiedConfidentialityImpact",
      options: confidentialityImpactOptions,
      title: translate.t(
        "searchFindings.tabSeverity.modifiedConfidentialityImpact"
      ),
    },
    {
      currentValue: dataset.modifiedIntegrityImpact,
      name: "modifiedIntegrityImpact",
      options: integrityImpactOptions,
      title: translate.t("searchFindings.tabSeverity.modifiedIntegrityImpact"),
    },
    {
      currentValue: dataset.modifiedAvailabilityImpact,
      name: "modifiedAvailabilityImpact",
      options: availabilityImpactOptions,
      title: translate.t(
        "searchFindings.tabSeverity.modifiedAvailabilityImpact"
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
          "searchFindings.tabSeverity.modifiedPrivilegesRequired"
        ),
      },
    ];
  }

  return fields;
};

export {
  attackComplexityBgColor,
  attackComplexityOptions,
  attackVectorBgColor,
  attackVectorOptions,
  availabilityImpactBgColor,
  availabilityImpactOptions,
  castFieldsCVSS3,
  castPrivileges,
  confidentialityImpactBgColor,
  confidentialityImpactOptions,
  exploitabilityBgColor,
  exploitabilityOptions,
  integrityImpactBgColor,
  integrityImpactOptions,
  remediationLevelBgColor,
  remediationLevelOptions,
  reportConfidenceBgColor,
  reportConfidenceOptions,
  severityScopeBgColor,
  severityScopeOptions,
  userInteractionBgColor,
  userInteractionOptions,
};
