import type { IVulnerabilityPoliciesData } from "scenes/Dashboard/containers/PoliciesView/Organization/VulnerabilityPolicies/types";
import type { IPoliciesData } from "scenes/Dashboard/containers/PoliciesView/types";

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
