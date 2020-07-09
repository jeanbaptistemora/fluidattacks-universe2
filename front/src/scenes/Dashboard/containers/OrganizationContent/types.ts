export interface IOrganizationContent {
  setUserRole(userRole: string | undefined): void;
}

export interface IOrganizationPermission {
  me: {
    permissions: string[];
    role: string | undefined;
  };
}
