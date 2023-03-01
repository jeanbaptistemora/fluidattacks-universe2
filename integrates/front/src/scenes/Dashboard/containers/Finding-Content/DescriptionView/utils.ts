import yaml from "js-yaml";
import _ from "lodash";

import type { IUnfulfilledRequirement } from "./types";

import type {
  IRequirementData,
  IVulnData,
} from "scenes/Dashboard/containers/Group-Content/GroupDraftsView/types";
import { translate } from "utils/translations/translate";

const BASE_URL: string =
  "https://gitlab.com/api/v4/projects/20741933/repository/files";
const BRANCH_REF: string = "trunk";
const REQUIREMENTS_FILE_ID: string =
  "common%2Fcriteria%2Fsrc%2Frequirements%2Fdata.yaml";

const formatFindingType: (type: string) => string = (type: string): string =>
  _.isEmpty(type)
    ? "-"
    : translate.t(`searchFindings.tabDescription.type.${type.toLowerCase()}`);

function formatRequirements(
  requirements: string[],
  criteriaData: Record<string, IRequirementData> | undefined
): IUnfulfilledRequirement[] {
  if (criteriaData === undefined || _.isEmpty(requirements)) {
    return [];
  }
  const requirementsData: IUnfulfilledRequirement[] = requirements.map(
    (key: string): IUnfulfilledRequirement => {
      return { id: key, summary: criteriaData[key].en.summary };
    }
  );

  return requirementsData;
}

function getRequirementsText(
  requirements: string[],
  criteriaData: Record<string, IRequirementData> | undefined,
  language?: string
): string[] {
  if (criteriaData === undefined || _.isEmpty(requirements)) {
    return requirements;
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

  return requirementsSummaries;
}

const getRequerimentsData = async (): Promise<
  Record<string, IRequirementData> | undefined
> => {
  const requirementsResponseFile: Response = await fetch(
    `${BASE_URL}/${REQUIREMENTS_FILE_ID}/raw?ref=${BRANCH_REF}`
  );
  const requirementsYamlFile: string = await requirementsResponseFile.text();

  return requirementsYamlFile
    ? (yaml.load(requirementsYamlFile) as Record<string, IRequirementData>)
    : undefined;
};

const getVulnsData = async (): Promise<
  Record<string, IVulnData> | undefined
> => {
  const vulnsFileId: string =
    "common%2Fcriteria%2Fsrc%2Fvulnerabilities%2Fdata.yaml";
  const vulnsResponseFile: Response = await fetch(
    `${BASE_URL}/${vulnsFileId}/raw?ref=${BRANCH_REF}`
  );
  const vulnsYamlFile: string = await vulnsResponseFile.text();

  return vulnsYamlFile
    ? (yaml.load(vulnsYamlFile) as Record<string, IVulnData>)
    : undefined;
};

export {
  formatFindingType,
  formatRequirements,
  getRequerimentsData,
  getRequirementsText,
  getVulnsData,
};
