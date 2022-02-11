interface IBillingAuthor {
  actor: string;
  commit: string;
  groups: string;
  organization: string;
  repository: string;
}

interface IBilling {
  authors: IBillingAuthor[];
}

interface IData {
  group: {
    billing: IBilling;
  };
}

export { IBillingAuthor, IBilling, IData };
