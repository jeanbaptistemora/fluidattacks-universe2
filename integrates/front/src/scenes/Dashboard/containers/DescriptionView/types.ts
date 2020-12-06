export interface IHistoricTreatment {
  acceptanceDate?: string;
  acceptanceStatus?: string;
  date: string;
  justification?: string;
  treatment: string;
  treatmentManager?: string;
  user: string;
}

export interface IFinding {
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
  state: "open" | "closed";
  threat: string;
  title: string;
  type: string;
}

export interface IFindingDescriptionData {
  finding: IFinding;
}

export interface IFindingDescriptionVars {
  canRetrieveAnalyst: boolean;
  canRetrieveSorts: boolean;
  findingId: string;
  projectName: string;
}
