export interface IDescriptionViewProps {
  dataset: {
    actor: string;
    affectedSystems: string;
    attackVector: string;
    btsUrl: string;
    compromisedAttributes: string;
    compromisedRecords: string;
    cweUrl: string;
    description: string;
    recommendation: string;
    releaseDate: string;
    remediated: boolean;
    reportLevel: string;
    requirements: string;
    scenario: string;
    state: string;
    subscription: string;
    threat: string;
    title: string;
    treatment: string;
    treatmentJustification: string;
    treatmentManager: string;
  };
  findingId: string;
  isEditing: boolean;
  isMdlConfirmOpen: boolean;
  isRemediationOpen: boolean;
  projectName: string;
  userRole: string;
}

