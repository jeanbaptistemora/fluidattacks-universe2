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
  seenAt: string;
  sortsRiskLevel: string;
}

export type {
  IGitRootAttr,
  IToeLinesAttr,
  IToeLinesConnection,
  IToeLinesData,
  IToeLinesEdge,
};
