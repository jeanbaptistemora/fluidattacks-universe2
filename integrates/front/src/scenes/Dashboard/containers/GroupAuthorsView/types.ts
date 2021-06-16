interface IBillAuthor {
  actor: string;
  commit: string;
  groups: string;
  organization: string;
  repository: string;
}

interface IBill {
  authors: IBillAuthor[];
}

interface IData {
  group: {
    bill: IBill;
  };
}

export { IBillAuthor, IBill, IData };
