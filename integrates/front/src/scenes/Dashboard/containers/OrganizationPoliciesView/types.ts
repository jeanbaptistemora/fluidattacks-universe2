export interface IOrganizationPolicies {
  organizationId: string;
}

export interface IPoliciesFormData {
  maxAcceptanceDays: string;
  maxAcceptanceSeverity: string;
  maxNumberAcceptations: string;
  minAcceptanceSeverity: string;
}
