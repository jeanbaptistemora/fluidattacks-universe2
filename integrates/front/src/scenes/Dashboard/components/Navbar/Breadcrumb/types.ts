interface IUserOrgs {
  me: {
    organizations: { name: string; groups: { name: string }[] }[];
    userEmail: string;
  };
}

interface IFindingTitle {
  finding: {
    title: string;
  };
}

export { IFindingTitle, IUserOrgs };
