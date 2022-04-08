interface IUserOrgs {
  me: {
    organizations: { name: string; groups: { name: string }[] }[];
    userEmail: string;
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

export { IFindingTitle, IUserOrgs, IUserTags };
