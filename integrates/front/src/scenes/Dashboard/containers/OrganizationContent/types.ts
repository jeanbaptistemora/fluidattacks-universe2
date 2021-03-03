interface IOrganizationContent {
  setUserRole: (userRole: string | undefined) => void;
}

interface IOrganizationPermission {
  me: {
    permissions: string[];
    role: string | undefined;
  };
}

export { IOrganizationContent, IOrganizationPermission };
