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

export interface IVerifyFindingResult {
  verifyFinding: {
    success: boolean;
  };
}

export interface IFinding {
  acceptanceDate: string;
  acceptationApproval: string;
  acceptationUser: string;
  actor: string;
  affectedSystems: string;
  attackVectorDesc: string;
  btsUrl: string;
  compromisedAttributes: string;
  compromisedRecords: string;
  cweUrl: string;
  description: string;
  historicTreatment: IHistoricTreatment[];
  justification: string;
  newRemediated: boolean;
  openVulnerabilities: number;
  recommendation: string;
  releaseDate: string;
  remediated: boolean;
  requirements: string;
  risk: string;
  scenario: string;
  state: string;
  threat: string;
  title: string;
  treatment: string;
  type: string;
  verified: boolean;
}
