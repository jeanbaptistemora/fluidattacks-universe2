interface IOrganizationContent {
  setUserRole: (userRole: string | undefined) => void;
}

interface IOrganizationPermission {
  organization: {
    permissions: string[];
    userRole: string | undefined;
  };
}

export { IOrganizationContent, IOrganizationPermission };
