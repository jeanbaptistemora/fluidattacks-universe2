interface IHistoricTreatment {
  acceptanceDate?: string;
  acceptanceStatus?: string;
  date: string;
  justification?: string;
  treatment: string;
  assigned?: string;
  user: string;
}

interface IUnfulfilledRequirement {
  id: string;
  summary: string;
}

interface IFinding {
  attackVectorDescription: string;
  description: string;
  hacker?: string;
  id: string;
  openVulnerabilities: number;
  recommendation: string;
  releaseDate: string | null;
  sorts: string;
  status: "SAFE" | "VULNERABLE";
  threat: string;
  title: string;
  unfulfilledRequirements: IUnfulfilledRequirement[];
}

interface IFindingDescriptionData {
  finding: IFinding;
}

interface IFindingDescriptionVars {
  canRetrieveHacker: boolean;
  canRetrieveSorts: boolean;
  findingId: string;
}

interface ILanguageData {
  group: {
    language: string;
  };
}

export type {
  IHistoricTreatment,
  IFinding,
  IFindingDescriptionData,
  IFindingDescriptionVars,
  ILanguageData,
  IUnfulfilledRequirement,
};
