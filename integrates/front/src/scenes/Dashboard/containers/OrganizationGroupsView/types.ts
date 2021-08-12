interface IGroupData {
  description: string;
  machine: string;
  squad: string;
  hasMachine: boolean;
  hasSquad: boolean;
  name: string;
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
