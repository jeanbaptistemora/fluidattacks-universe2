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

interface IOrganizationFindingTitles {
  organization: {
    id: string;
    groups: {
      name: string;
      findings: {
        id: string;
        title: string;
      }[];
    }[];
  };
}

export {
  IFindingPolicies,
  IFindingPoliciesData,
  IFindingPoliciesForm,
  IOrganizationFindingTitles,
};
