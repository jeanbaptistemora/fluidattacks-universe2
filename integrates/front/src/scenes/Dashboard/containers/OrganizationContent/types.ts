interface IOrganizationContent {
  setUserRole: (userRole: string | undefined) => void;
}

interface IOrganizationPermission {
  organization: {
    permissions: string[];
    userRole: string | undefined;
  };
}

interface IGetOrganizationId {
  organizationId: {
    id: string;
    name: string;
  };
}

export { IGetOrganizationId, IOrganizationContent, IOrganizationPermission };
