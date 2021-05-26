interface IBillDeveloper {
  actor: string;
  commit: string;
  groups: string;
  organization: string;
  repository: string;
}

interface IBill {
  developers: IBillDeveloper[];
}

interface IData {
  project: {
    bill: IBill;
  };
}

export { IBillDeveloper, IBill, IData };
