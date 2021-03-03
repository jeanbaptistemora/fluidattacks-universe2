interface IOrganizationPolicies {
  organizationId: string;
}

interface IPoliciesFormData {
  maxAcceptanceDays: string;
  maxAcceptanceSeverity: string;
  maxNumberAcceptations: string;
  minAcceptanceSeverity: string;
}

export { IOrganizationPolicies, IPoliciesFormData };
