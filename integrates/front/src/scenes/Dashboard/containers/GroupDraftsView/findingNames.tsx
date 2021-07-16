/* eslint-disable camelcase */
import yaml from "js-yaml";
import _ from "lodash";

import type {
  ISuggestion,
  IVulnData,
} from "scenes/Dashboard/containers/GroupDraftsView/types";
import { validateNotEmpty } from "scenes/Dashboard/containers/GroupDraftsView/utils";

const attackVectorOptions: Record<string, string> = {
  A: "0.62",
  L: "0.55",
  N: "0.85",
  P: "0.2",
};

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

        if (!_.isNil(language) && language === "ES") {
          return {
            attackVector,
            cwe,
            description: validateNotEmpty(vulnsData[key].es.description),
            recommendation: validateNotEmpty(vulnsData[key].es.recommendation),
            requirements: validateNotEmpty(
              vulnsData[key].requirements.toString()
            ),
            threat: validateNotEmpty(vulnsData[key].es.threat),
            title: validateNotEmpty(vulnsData[key].es.title),
          };
        }

        return {
          attackVector,
          cwe,
          description: validateNotEmpty(vulnsData[key].en.description),
          recommendation: validateNotEmpty(vulnsData[key].en.recommendation),
          requirements: validateNotEmpty(
            vulnsData[key].requirements.toString()
          ),
          threat: validateNotEmpty(vulnsData[key].en.threat),
          title: validateNotEmpty(vulnsData[key].en.title),
        };
      }
    );

    return suggestions;
  }

  return [];
}

export { getFindingNames };
