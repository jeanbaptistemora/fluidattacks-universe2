interface IUserOrgs {
  me: {
    organizations: { name: string }[];
    userEmail: string;
  };
}

interface IFindingTitle {
  finding: {
    title: string;
  };
}

export { IFindingTitle, IUserOrgs };
