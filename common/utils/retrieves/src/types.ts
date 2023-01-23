interface IGroup {
  name: string;
  subscription: string;
}

interface IOrganization {
  groups: IGroup[];
}

interface IGitRoot {
  id: string;
  nickname: string;
  state: "ACTIVE" | "INACTIVE";
  gitignore: string[];
  downloadUrl?: string;
}

interface IToeLinesPaginator {
  edges: {
    node: {
      attackedLines: number;
      filename: string;
      comments: string;
      modifiedDate: string;
      loc: number;
    };
  }[];
}

export type {
  IGroup as Group,
  IOrganization as Organization,
  IGitRoot as GitRoot,
  IToeLinesPaginator,
};
