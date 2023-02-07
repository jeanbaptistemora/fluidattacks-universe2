interface IAddGitRootResult {
  addGitRoot: {
    success: boolean;
  };
}

interface IAddGroupResult {
  addGroup: {
    success: boolean;
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

type IAlertMessages = React.Dispatch<
  React.SetStateAction<{
    message: string;
    type: string;
  }>
>;

interface ICheckGitAccessResult {
  validateGitAccess: {
    success: boolean;
  };
}

interface IGetStakeholderGroupsResult {
  me: {
    organizations: {
      country: string;
      groups: {
        name: string;
      }[];
      name: string;
    }[];
    trial: {
      completed: boolean;
      startDate: string;
    } | null;
    userEmail: string;
  };
}

interface IRootAttr {
  branch: string;
  credentials: {
    auth: "TOKEN" | "USER";
    azureOrganization: string | undefined;
    isPat: boolean | undefined;
    key: string;
    name: string;
    password: string;
    token: string;
    type: "" | "HTTPS" | "SSH";
    user: string;
  };
  env: string;
  exclusions: string[];
  url: string;
}

interface IOrgAttr {
  groupDescription: string;
  groupName: string;
  organizationCountry: string;
  organizationName: string;
  reportLanguage: string;
  terms: string[];
}

export type {
  IAddGitRootResult,
  IAddGroupResult,
  IAddOrganizationResult,
  IAlertMessages,
  ICheckGitAccessResult,
  IGetStakeholderGroupsResult,
  IOrgAttr,
  IRootAttr,
};
