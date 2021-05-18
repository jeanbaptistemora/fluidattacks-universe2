interface IFindingPolicies {
  organizationId: string;
}
interface IFindingPoliciesForm {
  name: string;
}

interface IOrganizationFindingTitles {
  organization: {
    id: string;
    projects: {
      name: string;
      findings: {
        id: string;
        title: string;
      }[];
    }[];
  };
}

export { IFindingPolicies, IFindingPoliciesForm, IOrganizationFindingTitles };
