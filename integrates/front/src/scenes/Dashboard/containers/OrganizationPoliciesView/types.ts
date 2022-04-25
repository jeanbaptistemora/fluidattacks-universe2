import type { IVulnerabilityPoliciesData } from "scenes/Dashboard/containers/OrganizationPoliciesView/VulnerabilityPolicies/types";

interface IOrganizationPolicies {
  organizationId: string;
}

interface IPoliciesFormData {
  maxAcceptanceDays: string;
  maxAcceptanceSeverity: string;
  maxNumberAcceptances: string;
  minAcceptanceSeverity: string;
  vulnerabilityGracePeriod: string;
  minBreakingSeverity: string;
}

interface IOrganizationPoliciesData {
  organization: {
    findingPolicies: IVulnerabilityPoliciesData[];
    maxAcceptanceDays: string;
    maxAcceptanceSeverity: string;
    maxNumberAcceptances: string;
    minAcceptanceSeverity: string;
    minBreakingSeverity: string;
    vulnerabilityGracePeriod: string;
    name: string;
  };
}

export type {
  IOrganizationPolicies,
  IOrganizationPoliciesData,
  IPoliciesFormData,
};
