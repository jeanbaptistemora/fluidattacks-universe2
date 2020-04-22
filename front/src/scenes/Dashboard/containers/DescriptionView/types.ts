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
  analyst: string;
  attackVectorDesc: string;
  btsUrl: string;
  compromisedAttributes: string;
  compromisedRecords: string;
  cweUrl: string;
  description: string;
  historicTreatment: IHistoricTreatment[];
  newRemediated: boolean;
  openVulnerabilities: number;
  recommendation: string;
  releaseDate: string;
  remediated: boolean;
  requirements: string;
  scenario: string;
  state: "open" | "closed";
  threat: string;
  title: string;
  type: string;
  verified: boolean;
}
