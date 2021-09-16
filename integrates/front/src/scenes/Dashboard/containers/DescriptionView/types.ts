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
  affectedSystems: string;
  attackVectorDescription: string;
  compromisedAttributes: string;
  compromisedRecords: number;
  description: string;
  hacker?: string;
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
  canRetrieveHacker: boolean;
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
