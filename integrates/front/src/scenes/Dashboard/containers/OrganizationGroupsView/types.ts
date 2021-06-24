interface IGroupData {
  description: string;
  squad: string;
  forces: string;
  hasSquad: boolean;
  hasForces: boolean;
  hasAsm: boolean;
  asm: string;
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
