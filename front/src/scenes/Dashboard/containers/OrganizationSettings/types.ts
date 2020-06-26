export interface ILocationState {
  state: {
    organizationId: string;
  };
}

export interface ISettingsFormData {
  maxAcceptanceDays: string;
  maxAcceptanceSeverity: string;
  maxNumberAcceptations: string;
  minAcceptanceSeverity: string;
}
