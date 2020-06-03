export interface IBillDeveloper {
  actor: string;
  commit: string;
  groups: string;
  organization: string;
  repository: string;
}

export interface IBill {
  developers: IBillDeveloper[];
}

export interface IData {
  project: {
    bill: IBill;
  };
}
