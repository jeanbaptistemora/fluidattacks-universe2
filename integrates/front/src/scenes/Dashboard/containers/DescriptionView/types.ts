export interface IAcceptationApprovalAttrs {
  handleAcceptation: {
    findingId: string;
    observations: string;
    projectName: string;
    response: string;
    success: boolean;
  };
}

export interface IHistoricTreatment {
  acceptanceDate?: string;
  acceptanceStatus?: string;
  date: string;
  justification?: string;
  treatment: string;
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
  historicTreatment: IHistoricTreatment[];
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
