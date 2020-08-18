export interface IGroupData {
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

export interface IOrganizationGroupsProps {
  organizationId: string;
}
