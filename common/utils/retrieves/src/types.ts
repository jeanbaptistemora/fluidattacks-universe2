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

interface IEdge {
  node: {
    attackedLines: number;
    filename: string;
    comments: string;
    modifiedDate: string;
    loc: number;
  };
}
interface IToeLinesPaginator {
  edges: IEdge[];
  pageInfo: {
    hasNextPage: boolean;
    endCursor: string;
  };
}

export type {
  IGroup as Group,
  IOrganization as Organization,
  IGitRoot as GitRoot,
  IToeLinesPaginator,
  IEdge,
};
