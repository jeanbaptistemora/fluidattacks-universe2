interface IHistoricTreatment {
  acceptanceDate?: string;
  acceptanceStatus?: string;
  date: string;
  justification?: string;
  treatment: string;
  treatmentManager?: string;
  user: string;
}

interface IFinding {
  actor: string;
  affectedSystems: string;
  analyst?: string;
  attackVectorDesc: string;
  compromisedAttributes: string;
  compromisedRecords: number;
  cweUrl: string;
  description: string;
  id: string;
  openVulnerabilities: number;
  recommendation: string;
  requirements: string;
  scenario: string;
  sorts: string;
  state: "closed" | "open";
  threat: string;
  title: string;
  type: string;
}

interface IFindingDescriptionData {
  finding: IFinding;
}

interface IFindingDescriptionVars {
  canRetrieveAnalyst: boolean;
  canRetrieveSorts: boolean;
  findingId: string;
  projectName: string;
}

export {
  IHistoricTreatment,
  IFinding,
  IFindingDescriptionData,
  IFindingDescriptionVars,
};
