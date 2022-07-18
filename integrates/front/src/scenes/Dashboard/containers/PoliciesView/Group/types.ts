import type { IPoliciesData } from "scenes/Dashboard/containers/PoliciesView/types";

interface IGroupPoliciesData {
  group: IPoliciesData & {
    name: string;
  };
}

export type { IGroupPoliciesData };
