export interface IGroupData {
    description: string;
    drills: string;
    forces: string;
    hasDrills: boolean;
    hasForces: boolean;
    name: string;
    userRole: string;
}

export interface IOrganizationGroupsProps {
  organizationId: string;
}
