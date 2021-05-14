interface IOrganizationPolicies {
  organizationId: string;
}

interface IPoliciesFormData {
  maxAcceptanceDays: string;
  maxAcceptanceSeverity: string;
  maxNumberAcceptations: string;
  minAcceptanceSeverity: string;
}

interface IOrganizationPoliciesData {
  organization: {
    maxAcceptanceDays: string;
    maxAcceptanceSeverity: string;
    maxNumberAcceptations: string;
    minAcceptanceSeverity: string;
    name: string;
  };
}

export { IOrganizationPolicies, IOrganizationPoliciesData, IPoliciesFormData };
