import type { IFindingPoliciesData } from "scenes/Dashboard/containers/OrganizationPoliciesView/FindingPolicies/types";

interface IOrganizationPolicies {
  organizationId: string;
}

interface IPoliciesFormData {
  maxAcceptanceDays: string;
  maxAcceptanceSeverity: string;
  maxNumberAcceptances: string;
  minAcceptanceSeverity: string;
}

interface IOrganizationPoliciesData {
  organization: {
    findingPolicies: IFindingPoliciesData[];
    maxAcceptanceDays: string;
    maxAcceptanceSeverity: string;
    maxNumberAcceptances: string;
    minAcceptanceSeverity: string;
    name: string;
  };
}

export { IOrganizationPolicies, IOrganizationPoliciesData, IPoliciesFormData };
