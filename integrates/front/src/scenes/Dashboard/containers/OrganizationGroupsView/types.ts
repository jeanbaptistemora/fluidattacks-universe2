interface IGroupData {
  description: string;
  squad: string;
  forces: string;
  hasDrills: boolean;
  hasForces: boolean;
  hasIntegrates: boolean;
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
