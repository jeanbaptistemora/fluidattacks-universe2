// eslint-disable camelcase
// Needed exception as the yaml file uses camelcase for its keys
import yaml from "js-yaml";
import _ from "lodash";

import type {
  IRequirementData,
  ISuggestion,
  IVulnData,
} from "scenes/Dashboard/containers/GroupDraftsView/types";
import { validateNotEmpty } from "scenes/Dashboard/containers/GroupDraftsView/utils";

// The following values are used also in SeverityView
const attackComplexityOptions: Record<string, string> = {
  H: "0.44",
  L: "0.77",
};

/*
 * P: physical
 * L: local
 * A: adjacent
 * N: network
 */
const attackVectorOptions: Record<string, string> = {
  A: "0.62",
  L: "0.55",
  N: "0.85",
  P: "0.2",
};

const availabilityImpactOptions: Record<string, string> = {
  H: "0.56",
  L: "0.22",
  N: "0",
};

const confidentialityImpactOptions: Record<string, string> = {
  H: "0.56",
  L: "0.22",
  N: "0",
};

/*
 * U: unproven
 * P: proof of concept
 * F: functional
 * H: high
 */
const exploitabilityOptions: Record<string, string> = {
  F: "0.97",
  H: "1",
  P: "0.94",
  U: "0.91",
};

const integrityImpactOptions: Record<string, string> = {
  H: "0.56",
  L: "0.22",
  N: "0",
};

const severityScopeOptions: Record<string, string> = {
  C: "1",
  U: "0",
};

const privilegesRequiredScope: Record<string, string> = {
  H: "0.5",
  L: "0.68",
  N: "0.85",
};

const privilegesRequiredNoScope: Record<string, string> = {
  H: "0.27",
  L: "0.62",
  N: "0.85",
};

/*
 * O: official fix
 * T: temporary fix
 * W: workaround
 * U: unavailable
 */
const remediationLevelOptions: Record<string, string> = {
  O: "0.95",
  T: "0.96",
  U: "1",
  W: "0.97",
};

/*
 * U: unknown
 * R: reasonable
 * C: confirmed
 */
const reportConfidenceOptions: Record<string, string> = {
  C: "1",
  R: "0.96",
  U: "0.92",
};

const userInteractionOptions: Record<string, string> = {
  N: "0.85",
  R: "0.62",
};

function getPrivilegesRequired(
  severityScope: string,
  privilegesRequired: string
): string {
  if (severityScope === severityScopeOptions.C) {
    return privilegesRequiredScope[privilegesRequired];
  }

  return privilegesRequiredNoScope[privilegesRequired];
}

function getRequirementsText(
  requirements: string[],
  language: string,
  criteriaData: Record<string, IRequirementData> | undefined
): string {
  if (criteriaData === undefined) {
    return requirements.toString();
  }
  const requirementsSummaries: string[] = requirements.map(
    (key: string): string => {
      const summary =
        language === "ES"
          ? criteriaData[key].es.summary
          : criteriaData[key].en.summary;

      return `${key}. ${summary}`;
    }
  );

  return requirementsSummaries.join("");
}

async function getFindingNames(
  language: string | undefined
): Promise<ISuggestion[]> {
  const baseUrl: string =
    "https://gitlab.com/api/v4/projects/20741933/repository/files";
  const branchRef: string = "master";

  const vulnsFileId: string =
    "makes%2Ffoss%2Fmodules%2Fmakes%2Fcriteria%2Fsrc%2Fvulnerabilities%2Fdata.yaml";
  const vulnsResponseFile: Response = await fetch(
    `${baseUrl}/${vulnsFileId}/raw?ref=${branchRef}`
  );
  const vulnsYamlFile: string = await vulnsResponseFile.text();
  const vulnsData = vulnsYamlFile
    ? (yaml.load(vulnsYamlFile) as Record<string, IVulnData>)
    : undefined;
  if (_.isNil(vulnsData)) {
    return [];
  }

  const requirementsFileId: string =
    "makes%2Ffoss%2Fmodules%2Fmakes%2Fcriteria%2Fsrc%2Frequirements%2Fdata.yaml";
  const requirementsResponseFile: Response = await fetch(
    `${baseUrl}/${requirementsFileId}/raw?ref=${branchRef}`
  );
  const requirementsYamlFile: string = await requirementsResponseFile.text();
  const requirementsData = requirementsYamlFile
    ? (yaml.load(requirementsYamlFile) as Record<string, IRequirementData>)
    : undefined;

  return Object.keys(vulnsData).map((key: string): ISuggestion => {
    const attackVectorRaw = validateNotEmpty(
      vulnsData[key].score.base.attack_vector
    );
    const attackVector =
      attackVectorRaw in attackVectorOptions
        ? attackVectorOptions[attackVectorRaw]
        : "0";
    const attackComplexityRaw = validateNotEmpty(
      vulnsData[key].score.base.attack_complexity
    );
    const attackComplexity =
      attackComplexityRaw in attackComplexityOptions
        ? attackComplexityOptions[attackComplexityRaw]
        : "0";
    const availabilityRaw = validateNotEmpty(
      vulnsData[key].score.base.availability
    );
    const availabilityImpact =
      availabilityRaw in availabilityImpactOptions
        ? availabilityImpactOptions[availabilityRaw]
        : "0";
    const confidentialityRaw = validateNotEmpty(
      vulnsData[key].score.base.confidentiality
    );
    const confidentialityImpact =
      confidentialityRaw in confidentialityImpactOptions
        ? confidentialityImpactOptions[confidentialityRaw]
        : "0";
    const exploitabilityRaw = validateNotEmpty(
      vulnsData[key].score.temporal.exploit_code_maturity
    );
    const exploitability =
      exploitabilityRaw in exploitabilityOptions
        ? exploitabilityOptions[exploitabilityRaw]
        : "0";
    const integrityRaw = validateNotEmpty(vulnsData[key].score.base.integrity);
    const integrityImpact =
      integrityRaw in integrityImpactOptions
        ? integrityImpactOptions[integrityRaw]
        : "0";
    const scopeRaw = validateNotEmpty(vulnsData[key].score.base.scope);
    const severityScope =
      scopeRaw in severityScopeOptions ? severityScopeOptions[scopeRaw] : "0";
    const privilegesRequiredRaw = validateNotEmpty(
      vulnsData[key].score.base.privileges_required
    );
    const privilegesRequired =
      privilegesRequiredRaw in privilegesRequiredScope
        ? getPrivilegesRequired(severityScope, privilegesRequiredRaw)
        : "0";
    const remediationLevelRaw = validateNotEmpty(
      vulnsData[key].score.temporal.remediation_level
    );
    const remediationLevel =
      remediationLevelRaw in remediationLevelOptions
        ? remediationLevelOptions[remediationLevelRaw]
        : "0";
    const reportConfidenceRaw = validateNotEmpty(
      vulnsData[key].score.temporal.report_confidence
    );
    const reportConfidence =
      reportConfidenceRaw in reportConfidenceOptions
        ? reportConfidenceOptions[reportConfidenceRaw]
        : "0";
    const userInteractionRaw = validateNotEmpty(
      vulnsData[key].score.base.user_interaction
    );
    const userInteraction =
      userInteractionRaw in userInteractionOptions
        ? userInteractionOptions[userInteractionRaw]
        : "0";
    const { requirements } = vulnsData[key];

    if (!_.isNil(language) && language === "ES") {
      return {
        attackComplexity,
        attackVector,
        attackVectorDescription: validateNotEmpty(vulnsData[key].es.impact),
        availabilityImpact,
        confidentialityImpact,
        description: validateNotEmpty(vulnsData[key].es.description),
        exploitability,
        integrityImpact,
        key,
        privilegesRequired,
        recommendation: validateNotEmpty(vulnsData[key].es.recommendation),
        remediationLevel,
        reportConfidence,
        requirements: getRequirementsText(requirements, "ES", requirementsData),
        severityScope,
        threat: validateNotEmpty(vulnsData[key].es.threat),
        title: validateNotEmpty(vulnsData[key].es.title),
        userInteraction,
      };
    }

    return {
      attackComplexity,
      attackVector,
      attackVectorDescription: validateNotEmpty(vulnsData[key].en.impact),
      availabilityImpact,
      confidentialityImpact,
      description: validateNotEmpty(vulnsData[key].en.description),
      exploitability,
      integrityImpact,
      key,
      privilegesRequired,
      recommendation: validateNotEmpty(vulnsData[key].en.recommendation),
      remediationLevel,
      reportConfidence,
      requirements: getRequirementsText(requirements, "EN", requirementsData),
      severityScope,
      threat: validateNotEmpty(vulnsData[key].en.threat),
      title: validateNotEmpty(vulnsData[key].en.title),
      userInteraction,
    };
  });
}

export { getFindingNames };
