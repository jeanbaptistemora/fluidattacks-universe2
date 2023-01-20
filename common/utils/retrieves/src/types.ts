interface IGroup {
  name: string;
  subscription: string;
}

interface IOrganization {
  groups: IGroup[];
}

interface IGitRoot {
  nickname: string;
  state: "ACTIVE" | "INACTIVE";
  gitignore: string[];
  downloadUrl?: string;
}

export type {
  IGroup as Group,
  IOrganization as Organization,
  IGitRoot as GitRoot,
};
