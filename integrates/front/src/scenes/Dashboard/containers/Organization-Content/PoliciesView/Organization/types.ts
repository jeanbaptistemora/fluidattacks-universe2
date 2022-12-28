import type { IVulnerabilityPoliciesData } from "scenes/Dashboard/containers/Organization-Content/PoliciesView/Organization/VulnerabilityPolicies/types";
import type { IPoliciesData } from "scenes/Dashboard/containers/Organization-Content/PoliciesView/types";

interface IOrganizationPolicies {
  organizationId: string;
}

interface IOrganizationPoliciesData {
  organization: IPoliciesData & {
    findingPolicies: IVulnerabilityPoliciesData[];
    name: string;
  };
}

export type { IOrganizationPolicies, IOrganizationPoliciesData };
