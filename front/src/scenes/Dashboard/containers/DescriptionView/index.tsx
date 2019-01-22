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
    reportLevel: string;
    requirements: string;
    scenario: string;
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
  userRole: string;
}

