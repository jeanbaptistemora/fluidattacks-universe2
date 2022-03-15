interface IGroupData {
  description: string;
  machine: string;
  squad: string;
  service: string;
  hasMachine: boolean;
  hasSquad: boolean;
  name: string;
  plan: string;
  subscription: string;
  userRole: string;
}

interface IOrganizationGroupsProps {
  organizationId: string;
}

interface IGetOrganizationGroups {
  organization: {
    groups: IGroupData[];
  };
}

export { IGroupData, IOrganizationGroupsProps, IGetOrganizationGroups };
