/* eslint-disable camelcase */
import yaml from "js-yaml";

interface ISuggestion {
  cwe: string;
  description: string;
  recommendation: string;
  requirements: string;
  title: string;
  type: string;
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

async function getFindingNames(): Promise<ISuggestion[]> {
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
        return {
          cwe: key,
          description: vulnsData[key].en.description,
          recommendation: vulnsData[key].en.recommendation,
          requirements: vulnsData[key].requirements.toString(),
          title: vulnsData[key].en.title,
          type: "",
        };
      }
    );

    return suggestions;
  }

  return [];
}

export { ISuggestion, getFindingNames };
