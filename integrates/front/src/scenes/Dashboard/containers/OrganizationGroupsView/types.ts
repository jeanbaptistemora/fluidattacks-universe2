interface IGroupData {
  description: string;
  drills: string;
  forces: string;
  hasDrills: boolean;
  hasForces: boolean;
  hasIntegrates: boolean;
  integrates: string;
  name: string;
  subscription: string;
  userRole: string;
}

interface IOrganizationGroupsProps {
  organizationId: string;
}

interface IGetOrganizationGroups {
  organization: {
    projects: IGroupData[];
  };
}

export { IGroupData, IOrganizationGroupsProps, IGetOrganizationGroups };
