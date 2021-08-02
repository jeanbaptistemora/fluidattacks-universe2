interface IFindingPolicies {
  findingPolicies: IFindingPoliciesData[];
  organizationId: string;
}
interface IFindingPoliciesData {
  id: string;
  name: string;
  status: "APPROVED" | "INACTIVE" | "REJECTED" | "SUBMITTED";
  lastStatusUpdate: string;
  tags: string[];
}
interface IFindingPoliciesForm {
  name: string;
  tags: string;
}

export { IFindingPolicies, IFindingPoliciesData, IFindingPoliciesForm };
