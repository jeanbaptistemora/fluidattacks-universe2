interface IUserOrgs {
  me: {
    organizations: { name: string }[];
    userEmail: string;
  };
}

interface IUserOrganizationGroupNames {
  organization: {
    groups: { name: string }[];
  };
}

interface IUserTags {
  me: {
    tags: { name: string }[];
    userEmail: string;
  };
}

interface IFindingTitle {
  finding: {
    title: string;
  };
}

export type {
  IFindingTitle,
  IUserOrgs,
  IUserOrganizationGroupNames,
  IUserTags,
};
