// eslint-disable camelcase
// Needed exception as the yaml file uses camelcase for its keys
import yaml from "js-yaml";
import _ from "lodash";

import type {
  ISuggestion,
  IVulnData,
} from "scenes/Dashboard/containers/GroupDraftsView/types";
import { validateNotEmpty } from "scenes/Dashboard/containers/GroupDraftsView/utils";

const attackComplexityOptions: Record<string, string> = {
  H: "0.44",
  L: "0.77",
};

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

async function getFindingNames(
  language: string | undefined
): Promise<ISuggestion[]> {
  const baseUrl: string =
    "https://gitlab.com/api/v4/projects/20741933/repository/files";
  const fileId: string =
    "makes%2Fapplications%2Fmakes%2Fcriteria%2Fsrc%2Fvulnerabilities%2Fdata.yaml";
  const branchRef: string = "master";
  const response: Response = await fetch(
    `${baseUrl}/${fileId}/raw?ref=${branchRef}`
  );
  const yamlFile: string = await response.text();
  if (yamlFile) {
    const vulnsData = yaml.load(yamlFile) as Record<string, IVulnData>;
    const suggestions: ISuggestion[] = Object.keys(vulnsData).map(
      (key: string): ISuggestion => {
        const cwe: string = key;
        const attackVectorRaw = vulnsData[key].score.base.attack_vector;
        const attackVector =
          attackVectorRaw in attackVectorOptions
            ? attackVectorOptions[attackVectorRaw]
            : "";
        const attackComplexityRaw = vulnsData[key].score.base.attack_complexity;
        const attackComplexity =
          attackComplexityRaw in attackComplexityOptions
            ? attackComplexityOptions[attackComplexityRaw]
            : "";
        const availabilityRaw = vulnsData[key].score.base.availability;
        const availabilityImpact =
          availabilityRaw in availabilityImpactOptions
            ? availabilityImpactOptions[availabilityRaw]
            : "";
        const confidentialityRaw = vulnsData[key].score.base.confidentiality;
        const confidentialityImpact =
          confidentialityRaw in confidentialityImpactOptions
            ? confidentialityImpactOptions[confidentialityRaw]
            : "";
        const integrityRaw = vulnsData[key].score.base.integrity;
        const integrityImpact =
          integrityRaw in integrityImpactOptions
            ? integrityImpactOptions[integrityRaw]
            : "";
        const scopeRaw = vulnsData[key].score.base.scope;
        const severityScope =
          scopeRaw in severityScopeOptions
            ? severityScopeOptions[scopeRaw]
            : "";
        const privilegesRequiredRaw =
          vulnsData[key].score.base.privileges_required;
        const privilegesRequired =
          privilegesRequiredRaw in privilegesRequiredScope
            ? getPrivilegesRequired(severityScope, privilegesRequiredRaw)
            : "";
        const userInteractionRaw = vulnsData[key].score.base.user_interaction;
        const userInteraction =
          userInteractionRaw in userInteractionOptions
            ? userInteractionOptions[userInteractionRaw]
            : "";

        if (!_.isNil(language) && language === "ES") {
          return {
            attackComplexity,
            attackVector,
            availabilityImpact,
            confidentialityImpact,
            cwe,
            description: validateNotEmpty(vulnsData[key].es.description),
            integrityImpact,
            privilegesRequired,
            recommendation: validateNotEmpty(vulnsData[key].es.recommendation),
            requirements: validateNotEmpty(
              vulnsData[key].requirements.toString()
            ),
            severityScope,
            threat: validateNotEmpty(vulnsData[key].es.threat),
            title: validateNotEmpty(vulnsData[key].es.title),
            userInteraction,
          };
        }

        return {
          attackComplexity,
          attackVector,
          availabilityImpact,
          confidentialityImpact,
          cwe,
          description: validateNotEmpty(vulnsData[key].en.description),
          integrityImpact,
          privilegesRequired,
          recommendation: validateNotEmpty(vulnsData[key].en.recommendation),
          requirements: validateNotEmpty(
            vulnsData[key].requirements.toString()
          ),
          severityScope,
          threat: validateNotEmpty(vulnsData[key].en.threat),
          title: validateNotEmpty(vulnsData[key].en.title),
          userInteraction,
        };
      }
    );

    return suggestions;
  }

  return [];
}

export { getFindingNames };
