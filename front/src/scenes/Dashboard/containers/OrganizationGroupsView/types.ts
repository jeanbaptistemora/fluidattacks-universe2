interface IGroupData {
    description: string;
    name: string;
}

export interface IOrganizationGroups {
    data: {
      organization: {
        projects: IGroupData[];
      };
    };
  }

export interface IOrganizationGroupsProps {
  organizationId: string;
}
