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

interface IGetUserPortfolios {
  me: {
    tags: {
      name: string;
      groups: {
        name: string;
      }[];
    }[];
    userEmail: string;
  };
}

export type {
  IGetOrganizationId,
  IGetUserPortfolios,
  IOrganizationContent,
  IOrganizationPermission,
};
