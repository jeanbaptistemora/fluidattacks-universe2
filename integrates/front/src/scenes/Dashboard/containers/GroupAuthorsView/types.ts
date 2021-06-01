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
  group: {
    bill: IBill;
  };
}

export { IBillDeveloper, IBill, IData };
