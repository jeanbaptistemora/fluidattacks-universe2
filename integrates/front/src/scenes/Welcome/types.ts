interface IGetUserWelcomeResult {
  me: {
    userEmail: string;
    organizations: {
      name: string;
    }[];
  };
}

interface IGetNewOrganizationNameResult {
  internalNames: {
    name: string;
  };
}

interface IAddOrganizationResult {
  addOrganization: {
    organization: {
      id: string;
      name: string;
    };
    success: boolean;
  };
}

interface IAutoenrollDemoResult {
  autoenrollDemo: {
    success: boolean;
  };
}

export type {
  IAddOrganizationResult,
  IAutoenrollDemoResult,
  IGetNewOrganizationNameResult,
  IGetUserWelcomeResult,
};
