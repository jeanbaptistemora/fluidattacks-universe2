import { translate } from "utils/translations/translate";
import type {
  ISeverityAttr,
  ISeverityField,
} from "scenes/Dashboard/containers/SeverityView/types";

const castPrivileges: (scope: string) => Record<string, string> = (
  scope: string
): Record<string, string> => {
  const privilegesRequiredScope: Record<string, string> = {
    0.5: "search_findings.tab_severity.privileges_required_options.high.text",
    0.68: "search_findings.tab_severity.privileges_required_options.low.text",
    0.85: "search_findings.tab_severity.privileges_required_options.none.text",
  };
  const privilegesRequiredNoScope: Record<string, string> = {
    0.27: "search_findings.tab_severity.privileges_required_options.high.text",
    0.62: "search_findings.tab_severity.privileges_required_options.low.text",
    0.85: "search_findings.tab_severity.privileges_required_options.none.text",
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
    0.2: "search_findings.tab_severity.attack_vector_options.physical.text",
    0.55: "search_findings.tab_severity.attack_vector_options.local.text",
    0.62: "search_findings.tab_severity.attack_vector_options.adjacent.text",
    0.85: "search_findings.tab_severity.attack_vector_options.network.text",
  };

  const attackComplexity: Record<string, string> = {
    0.44: "search_findings.tab_severity.attack_complexity_options.high.text",
    0.77: "search_findings.tab_severity.attack_complexity_options.low.text",
  };

  const userInteraction: Record<string, string> = {
    0.62: "search_findings.tab_severity.user_interaction_options.required.text",
    0.85: "search_findings.tab_severity.user_interaction_options.none.text",
  };

  const severityScope: Record<string, string> = {
    0: "search_findings.tab_severity.severity_scope_options.unchanged.text",
    1: "search_findings.tab_severity.severity_scope_options.changed.text",
  };

  const confidentialityImpact: Record<string, string> = {
    0: "search_findings.tab_severity.confidentiality_impact_options.none.text",
    0.22: "search_findings.tab_severity.confidentiality_impact_options.low.text",
    0.56: "search_findings.tab_severity.confidentiality_impact_options.high.text",
  };

  const integrityImpact: Record<string, string> = {
    0: "search_findings.tab_severity.integrity_impact_options.none.text",
    0.22: "search_findings.tab_severity.integrity_impact_options.low.text",
    0.56: "search_findings.tab_severity.integrity_impact_options.high.text",
  };

  const availabilityImpact: Record<string, string> = {
    0: "search_findings.tab_severity.availability_impact_options.none.text",
    0.22: "search_findings.tab_severity.availability_impact_options.low.text",
    0.56: "search_findings.tab_severity.availability_impact_options.high.text",
  };

  const exploitability: Record<string, string> = {
    0.91: "search_findings.tab_severity.exploitability_options.unproven.text",
    0.94: "search_findings.tab_severity.exploitability_options.proof_of_concept.text",
    0.97: "search_findings.tab_severity.exploitability_options.functional.text",
    1: "search_findings.tab_severity.exploitability_options.high.text",
  };

  const remediationLevel: Record<string, string> = {
    0.95: "search_findings.tab_severity.remediation_level_options.official_fix.text",
    0.96: "search_findings.tab_severity.remediation_level_options.temporary_fix.text",
    0.97: "search_findings.tab_severity.remediation_level_options.workaround.text",
    1: "search_findings.tab_severity.remediation_level_options.unavailable.text",
  };

  const reportConfidence: Record<string, string> = {
    0.92: "search_findings.tab_severity.report_confidence_options.unknown.text",
    0.96: "search_findings.tab_severity.report_confidence_options.reasonable.text",
    1: "search_findings.tab_severity.report_confidence_options.confirmed.text",
  };

  const fields: ISeverityField[] = [
    {
      currentValue: dataset.attackVector,
      name: "attackVector",
      options: attackVector,
      title: translate.t("search_findings.tab_severity.attack_vector"),
    },
    {
      currentValue: dataset.attackComplexity,
      name: "attackComplexity",
      options: attackComplexity,
      title: translate.t("search_findings.tab_severity.attack_complexity"),
    },
    {
      currentValue: dataset.userInteraction,
      name: "userInteraction",
      options: userInteraction,
      title: translate.t("search_findings.tab_severity.user_interaction"),
    },
    {
      currentValue: dataset.severityScope,
      name: "severityScope",
      options: severityScope,
      title: translate.t("search_findings.tab_severity.severity_scope"),
    },
    {
      currentValue: dataset.confidentialityImpact,
      name: "confidentialityImpact",
      options: confidentialityImpact,
      title: translate.t("search_findings.tab_severity.confidentiality_impact"),
    },
    {
      currentValue: dataset.integrityImpact,
      name: "integrityImpact",
      options: integrityImpact,
      title: translate.t("search_findings.tab_severity.integrity_impact"),
    },
    {
      currentValue: dataset.availabilityImpact,
      name: "availabilityImpact",
      options: availabilityImpact,
      title: translate.t("search_findings.tab_severity.availability_impact"),
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
      title: translate.t("search_findings.tab_severity.remediation_level"),
    },
    {
      currentValue: dataset.reportConfidence,
      name: "reportConfidence",
      options: reportConfidence,
      title: translate.t("search_findings.tab_severity.report_confidence"),
    },
    {
      currentValue: dataset.privilegesRequired,
      name: "privilegesRequired",
      options: castPrivileges(formValues.severityScope),
      title: translate.t("search_findings.tab_severity.privileges_required"),
    },
  ];

  const confidentialityRequirement: Record<string, string> = {
    0.5: "search_findings.tab_severity.confidentiality_requirement_options.low.text",
    1: "search_findings.tab_severity.confidentiality_requirement_options.medium.text",
    1.5: "search_findings.tab_severity.confidentiality_requirement_options.high.text",
  };

  const integrityRequirement: Record<string, string> = {
    0.5: "search_findings.tab_severity.integrity_requirement_options.low.text",
    1: "search_findings.tab_severity.integrity_requirement_options.medium.text",
    1.5: "search_findings.tab_severity.integrity_requirement_options.high.text",
  };

  const availabilityRequirement: Record<string, string> = {
    0.5: "search_findings.tab_severity.availability_requirement_options.low.text",
    1: "search_findings.tab_severity.availability_requirement_options.medium.text",
    1.5: "search_findings.tab_severity.availability_requirement_options.high.text",
  };

  const environmentFields: ISeverityField[] = [
    {
      currentValue: dataset.confidentialityRequirement,
      name: "confidentialityRequirement",
      options: confidentialityRequirement,
      title: translate.t(
        "search_findings.tab_severity.confidentiality_requirement"
      ),
    },
    {
      currentValue: dataset.integrityRequirement,
      name: "integrityRequirement",
      options: integrityRequirement,
      title: translate.t("search_findings.tab_severity.integrity_requirement"),
    },
    {
      currentValue: dataset.availabilityRequirement,
      name: "availabilityRequirement",
      options: availabilityRequirement,
      title: translate.t(
        "search_findings.tab_severity.availability_requirement"
      ),
    },
    {
      currentValue: dataset.modifiedAttackVector,
      name: "modifiedAttackVector",
      options: attackVector,
      title: translate.t("search_findings.tab_severity.modified_attack_vector"),
    },
    {
      currentValue: dataset.modifiedAttackComplexity,
      name: "modifiedAttackComplexity",
      options: attackComplexity,
      title: translate.t(
        "search_findings.tab_severity.modified_attack_complexity"
      ),
    },
    {
      currentValue: dataset.modifiedUserInteraction,
      name: "modifiedUserInteraction",
      options: userInteraction,
      title: translate.t(
        "search_findings.tab_severity.modified_user_interaction"
      ),
    },
    {
      currentValue: dataset.modifiedSeverityScope,
      name: "modifiedSeverityScope",
      options: severityScope,
      title: translate.t(
        "search_findings.tab_severity.modified_severity_scope"
      ),
    },
    {
      currentValue: dataset.modifiedConfidentialityImpact,
      name: "modifiedConfidentialityImpact",
      options: confidentialityImpact,
      title: translate.t(
        "search_findings.tab_severity.modified_confidentiality_impact"
      ),
    },
    {
      currentValue: dataset.modifiedIntegrityImpact,
      name: "modifiedIntegrityImpact",
      options: integrityImpact,
      title: translate.t(
        "search_findings.tab_severity.modified_integrity_impact"
      ),
    },
    {
      currentValue: dataset.modifiedAvailabilityImpact,
      name: "modifiedAvailabilityImpact",
      options: availabilityImpact,
      title: translate.t(
        "search_findings.tab_severity.modified_availability_impact"
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
          "search_findings.tab_severity.modified_privileges_required"
        ),
      },
    ];
  }

  return fields;
};
