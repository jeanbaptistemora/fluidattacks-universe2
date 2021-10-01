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
  attackVectorDescription: string;
  compromisedAttributes: string;
  compromisedRecords: number;
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
  groupName: string;
}

export {
  IHistoricTreatment,
  IFinding,
  IFindingDescriptionData,
  IFindingDescriptionVars,
};
