interface IToeLinesEdge {
  node: IToeLinesAttr;
}

interface IToeLinesConnection {
  edges: IToeLinesEdge[];
  pageInfo: {
    hasNextPage: boolean;
    endCursor: string;
  };
}

interface IToeLinesAttr {
  attackedAt: string;
  attackedBy: string;
  attackedLines: number;
  bePresent: boolean;
  bePresentUntil: string;
  comments: string;
  commitAuthor: string;
  filename: string;
  firstAttackAt: string;
  loc: number;
  modifiedCommit: string;
  modifiedDate: string;
  root: IGitRootAttr;
  seenAt: string;
  sortsRiskLevel: number;
}

interface IGitRootAttr {
  id: string;
  nickname: string;
}

interface IToeLinesData {
  attackedAt: string;
  attackedBy: string;
  attackedLines: number;
  bePresent: boolean;
  bePresentUntil: string;
  comments: string;
  commitAuthor: string;
  coverage: number;
  daysToAttack: number;
  filename: string;
  firstAttackAt: string;
  loc: number;
  modifiedCommit: string;
  modifiedDate: string;
  root: IGitRootAttr;
  rootNickname: string;
  rootId: string;
  seenAt: string;
  sortsRiskLevel: string;
}

interface IGroupToeLinesViewProps {
  isInternal: boolean;
}

export type {
  IGitRootAttr,
  IGroupToeLinesViewProps,
  IToeLinesAttr,
  IToeLinesConnection,
  IToeLinesData,
  IToeLinesEdge,
};
