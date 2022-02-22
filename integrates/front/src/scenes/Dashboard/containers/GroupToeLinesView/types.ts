interface IFilterSet {
  bePresent: string;
  coverage: { max: string; min: string };
  filenameExtension: string;
  hasVulnerabilities: string;
  modifiedDate: { max: string; min: string };
  priority: { max: string; min: string };
  rootId: string;
  seenAt: { max: string; min: string };
}
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
  attackedAt: string | null;
  attackedBy: string;
  attackedLines: number;
  bePresent: boolean;
  bePresentUntil: string | null;
  comments: string;
  filename: string;
  firstAttackAt: string | null;
  hasVulnerabilities: boolean;
  lastAuthor: string;
  lastCommit: string;
  loc: number;
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
  attackedAt: Date | undefined;
  attackedBy: string;
  attackedLines: number;
  bePresent: boolean;
  bePresentUntil: Date | undefined;
  comments: string;
  coverage: number;
  daysToAttack: number;
  extension: string;
  filename: string;
  firstAttackAt: Date | undefined;
  hasVulnerabilities: boolean;
  lastAuthor: string;
  lastCommit: string;
  loc: number;
  modifiedDate: Date | undefined;
  root: IGitRootAttr;
  rootNickname: string;
  rootId: string;
  seenAt: Date | undefined;
  sortsRiskLevel: number;
}

interface IGroupToeLinesViewProps {
  isInternal: boolean;
}

export type {
  IFilterSet,
  IGitRootAttr,
  IGroupToeLinesViewProps,
  IToeLinesAttr,
  IToeLinesConnection,
  IToeLinesData,
  IToeLinesEdge,
};
