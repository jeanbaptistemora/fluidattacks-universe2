import type {
  ISeverityAttr,
  ISeverityField,
} from "scenes/Dashboard/containers/SeverityView/types";
import { translate } from "utils/translations/translate";

const castPrivileges: (scope: string) => Record<string, string> = (
  scope: string
): Record<string, string> => {
  const privilegesRequiredScope: Record<string, string> = {
    0.5: "searchFindings.tabSeverity.privilegesRequired.options.high.label",
    0.68: "searchFindings.tabSeverity.privilegesRequired.options.low.label",
    0.85: "searchFindings.tabSeverity.privilegesRequired.options.none.label",
  };
  const privilegesRequiredNoScope: Record<string, string> = {
    0.27: "searchFindings.tabSeverity.privilegesRequired.options.high.label",
    0.62: "searchFindings.tabSeverity.privilegesRequired.options.low.label",
    0.85: "searchFindings.tabSeverity.privilegesRequired.options.none.label",
  };

  if (parseInt(scope, 10) === 1) {
    return privilegesRequiredScope;
  }

  return privilegesRequiredNoScope;
};

const attackComplexityBgColor: Record<string, string> = {
  0.44: "bg-lbl-yellow",
  0.77: "bg-dark-red",
};

const attackComplexityOptions: Record<string, string> = {
  0.44: "searchFindings.tabSeverity.attackComplexity.options.high.label",
  0.77: "searchFindings.tabSeverity.attackComplexity.options.low.label",
};

const attackVectorBgColor: Record<string, string> = {
  0.2: "bg-lbl-yellow",
  0.55: "bg-orange",
  0.62: "bg-red",
  0.85: "bg-dark-red",
};

const attackVectorOptions: Record<string, string> = {
  0.2: "searchFindings.tabSeverity.attackVector.options.physical.label",
  0.55: "searchFindings.tabSeverity.attackVector.options.local.label",
  0.62: "searchFindings.tabSeverity.attackVector.options.adjacent.label",
  0.85: "searchFindings.tabSeverity.attackVector.options.network.label",
};

const availabilityImpactBgColor: Record<string, string> = {
  0: "bg-lbl-green",
  0.22: "bg-lbl-yellow",
  0.56: "bg-dark-red",
};

const availabilityImpactOptions: Record<string, string> = {
  0: "searchFindings.tabSeverity.availabilityImpact.options.none.label",
  0.22: "searchFindings.tabSeverity.availabilityImpact.options.low.label",
  0.56: "searchFindings.tabSeverity.availabilityImpact.options.high.label",
};

const confidentialityImpactBgColor: Record<string, string> = {
  0: "bg-lbl-green",
  0.22: "bg-lbl-yellow",
  0.56: "bg-dark-red",
};

const confidentialityImpactOptions: Record<string, string> = {
  0: "searchFindings.tabSeverity.confidentialityImpact.options.none.label",
  0.22: "searchFindings.tabSeverity.confidentialityImpact.options.low.label",
  0.56: "searchFindings.tabSeverity.confidentialityImpact.options.high.label",
};

const exploitabilityBgColor: Record<string, string> = {
  0.91: "bg-lbl-yellow",
  0.94: "bg-orange",
  0.97: "bg-red",
  1: "bg-dark-red",
};

const exploitabilityOptions: Record<string, string> = {
  0.91: "searchFindings.tabSeverity.exploitability.options.unproven.label",
  0.94: "searchFindings.tabSeverity.exploitability.options.proofOfConcept.label",
  0.97: "searchFindings.tabSeverity.exploitability.options.functional.label",
  1: "searchFindings.tabSeverity.exploitability.options.high.label",
};

const integrityImpactBgColor: Record<string, string> = {
  0: "bg-lbl-green",
  0.22: "bg-lbl-yellow",
  0.56: "bg-dark-red",
};

const integrityImpactOptions: Record<string, string> = {
  0: "searchFindings.tabSeverity.integrityImpact.options.none.label",
  0.22: "searchFindings.tabSeverity.integrityImpact.options.low.label",
  0.56: "searchFindings.tabSeverity.integrityImpact.options.high.label",
};

const remediationLevelBgColor: Record<string, string> = {
  0.95: "bg-lbl-green",
  0.96: "bg-lbl-yellow",
  0.97: "bg-orange",
  1: "bg-dark-red",
};

const remediationLevelOptions: Record<string, string> = {
  0.95: "searchFindings.tabSeverity.remediationLevel.options.officialFix.label",
  0.96: "searchFindings.tabSeverity.remediationLevel.options.temporaryFix.label",
  0.97: "searchFindings.tabSeverity.remediationLevel.options.workaround.label",
  1: "searchFindings.tabSeverity.remediationLevel.options.unavailable.label",
};

const reportConfidenceBgColor: Record<string, string> = {
  0.92: "bg-lbl-yellow",
  0.96: "bg-orange",
  1: "bg-dark-red",
};

const reportConfidenceOptions: Record<string, string> = {
  0.92: "searchFindings.tabSeverity.reportConfidence.options.unknown.label",
  0.96: "searchFindings.tabSeverity.reportConfidence.options.reasonable.label",
  1: "searchFindings.tabSeverity.reportConfidence.options.confirmed.label",
};

const severityScopeBgColor: Record<string, string> = {
  0: "bg-lbl-yellow",
  1: "bg-dark-red",
};

const severityScopeOptions: Record<string, string> = {
  0: "searchFindings.tabSeverity.severityScope.options.unchanged.label",
  1: "searchFindings.tabSeverity.severityScope.options.changed.label",
};

const userInteractionBgColor: Record<string, string> = {
  0.62: "bg-lbl-yellow",
  0.85: "bg-dark-red",
};

const userInteractionOptions: Record<string, string> = {
  0.62: "searchFindings.tabSeverity.userInteraction.options.required.label",
  0.85: "searchFindings.tabSeverity.userInteraction.options.none.label",
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
      title: translate.t("searchFindings.tabSeverity.attackVector.label"),
    },
    {
      currentValue: dataset.attackComplexity,
      name: "attackComplexity",
      options: attackComplexityOptions,
      title: translate.t("searchFindings.tabSeverity.attackComplexity.label"),
    },
    {
      currentValue: dataset.userInteraction,
      name: "userInteraction",
      options: userInteractionOptions,
      title: translate.t("searchFindings.tabSeverity.userInteraction.label"),
    },
    {
      currentValue: dataset.severityScope,
      name: "severityScope",
      options: severityScopeOptions,
      title: translate.t("searchFindings.tabSeverity.severityScope.label"),
    },
    {
      currentValue: dataset.confidentialityImpact,
      name: "confidentialityImpact",
      options: confidentialityImpactOptions,
      title: translate.t(
        "searchFindings.tabSeverity.confidentialityImpact.label"
      ),
    },
    {
      currentValue: dataset.integrityImpact,
      name: "integrityImpact",
      options: integrityImpactOptions,
      title: translate.t("searchFindings.tabSeverity.integrityImpact.label"),
    },
    {
      currentValue: dataset.availabilityImpact,
      name: "availabilityImpact",
      options: availabilityImpactOptions,
      title: translate.t("searchFindings.tabSeverity.availabilityImpact.label"),
    },
    {
      currentValue: dataset.exploitability,
      name: "exploitability",
      options: exploitabilityOptions,
      title: translate.t("searchFindings.tabSeverity.exploitability.label"),
    },
    {
      currentValue: dataset.remediationLevel,
      name: "remediationLevel",
      options: remediationLevelOptions,
      title: translate.t("searchFindings.tabSeverity.remediationLevel.label"),
    },
    {
      currentValue: dataset.reportConfidence,
      name: "reportConfidence",
      options: reportConfidenceOptions,
      title: translate.t("searchFindings.tabSeverity.reportConfidence.label"),
    },
    {
      currentValue: dataset.privilegesRequired,
      name: "privilegesRequired",
      options: castPrivileges(formValues.severityScope),
      title: translate.t("searchFindings.tabSeverity.privilegesRequired.label"),
    },
  ];

  const confidentialityRequirement: Record<string, string> = {
    0.5: "searchFindings.tabSeverity.confidentialityRequirement.options.low.label",
    1: "searchFindings.tabSeverity.confidentialityRequirement.options.medium.label",
    1.5: "searchFindings.tabSeverity.confidentialityRequirement.options.high.label",
  };

  const integrityRequirement: Record<string, string> = {
    0.5: "searchFindings.tabSeverity.integrityRequirement.options.low.label",
    1: "searchFindings.tabSeverity.integrityRequirement.options.medium.label",
    1.5: "searchFindings.tabSeverity.integrityRequirement.options.high.label",
  };

  const availabilityRequirement: Record<string, string> = {
    0.5: "searchFindings.tabSeverity.availabilityRequirement.options.low.label",
    1: "searchFindings.tabSeverity.availabilityRequirement.options.medium.label",
    1.5: "searchFindings.tabSeverity.availabilityRequirement.options.high.label",
  };

  const environmentFields: ISeverityField[] = [
    {
      currentValue: dataset.confidentialityRequirement,
      name: "confidentialityRequirement",
      options: confidentialityRequirement,
      title: translate.t(
        "searchFindings.tabSeverity.confidentialityRequirement.label"
      ),
    },
    {
      currentValue: dataset.integrityRequirement,
      name: "integrityRequirement",
      options: integrityRequirement,
      title: translate.t(
        "searchFindings.tabSeverity.integrityRequirement.label"
      ),
    },
    {
      currentValue: dataset.availabilityRequirement,
      name: "availabilityRequirement",
      options: availabilityRequirement,
      title: translate.t(
        "searchFindings.tabSeverity.availabilityRequirement.label"
      ),
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
