import type { IFindingPoliciesData } from "scenes/Dashboard/containers/OrganizationPoliciesView/FindingPolicies/types";

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
    findingPolicies: IFindingPoliciesData[];
    maxAcceptanceDays: string;
    maxAcceptanceSeverity: string;
    maxNumberAcceptations: string;
    minAcceptanceSeverity: string;
    name: string;
  };
}

export { IOrganizationPolicies, IOrganizationPoliciesData, IPoliciesFormData };
