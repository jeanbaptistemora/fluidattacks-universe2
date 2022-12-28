import type { IPoliciesData } from "scenes/Dashboard/containers/Organization-Content/PoliciesView/types";

interface IGroupPoliciesData {
  group: IPoliciesData & {
    name: string;
  };
}

export type { IGroupPoliciesData };
