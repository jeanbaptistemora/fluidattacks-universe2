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
  groupName: string;
  state: "ACTIVE" | "INACTIVE";
  gitignore: string[];
  downloadUrl?: string;
  gitEnvironmentUrls: {
    id: string;
    url: string;
  }[];
}
interface IToeLineNode {
  attackedLines: number;
  filename: string;
  comments: string;
  modifiedDate: string;
  loc: number;
}
interface IEdge {
  node: IToeLineNode;
}
interface IToeLinesPaginator {
  edges: IEdge[];
  pageInfo: {
    hasNextPage: boolean;
    endCursor: string;
  };
}

interface IVulnerability {
  id: string;
  specific: string;
  where: string;
  rootNickname: string;
  state: "REJECTED" | "SAFE" | "SUBMITTED" | "VULNERABLE";
  finding: IFinding;
}

interface IFinding {
  description: string;
  id: string;
  title: string;
}

export type {
  IGroup as Group,
  IOrganization as Organization,
  IGitRoot,
  IToeLinesPaginator,
  IEdge,
  IToeLineNode,
  IVulnerability,
  IFinding,
};
