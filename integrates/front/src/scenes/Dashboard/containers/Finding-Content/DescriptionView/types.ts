interface IHistoricTreatment {
  acceptanceDate?: string;
  acceptanceStatus?: string;
  date: string;
  justification?: string;
  treatment: string;
  assigned?: string;
  user: string;
}

interface IFinding {
  attackVectorDescription: string;
  description: string;
  hacker?: string;
  id: string;
  openVulnerabilities: number;
  recommendation: string;
  releaseDate: string | null;
  requirements: string;
  sorts: string;
  status: "SAFE" | "VULNERABLE";
  threat: string;
  title: string;
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
};
