interface IFilterSet {
  address: string;
  bePresent: string;
  hasVulnerabilities: string;
  rootId: string;
  seenAt: { max: string; min: string };
  seenFirstTimeBy: string;
}

interface IGroupToePortsViewProps {
  isInternal: boolean;
}

interface IToePortEdge {
  node: IToePortAttr;
}

interface IToePortsConnection {
  edges: IToePortEdge[];
  pageInfo: {
    hasNextPage: boolean;
    endCursor: string;
  };
}
interface IToePortAttr {
  address: string;
  attackedAt: string | null;
  attackedBy: string;
  bePresent: boolean;
  bePresentUntil: string | null;
  firstAttackAt: string | null;
  hasVulnerabilities: boolean;
  port: string;
  root: IIPRootAttr | null;
  seenAt: string | null;
  seenFirstTimeBy: string;
}

interface IIPRootAttr {
  id: string;
  nickname: string;
}

interface IToePortData {
  attackedAt: Date | undefined;
  attackedBy: string;
  bePresent: boolean;
  bePresentUntil: Date | undefined;
  address: string;
  port: string;
  firstAttackAt: Date | undefined;
  hasVulnerabilities: boolean;
  markedSeenFirstTimeBy: string;
  root: IIPRootAttr | null;
  rootId: string;
  rootNickname: string;
  seenAt: Date | undefined;
  seenFirstTimeBy: string;
}

interface IUpdateToePortResultAttr {
  updateToePort: {
    success: boolean;
    toePort: IToePortAttr | undefined;
  };
}

export type {
  IFilterSet,
  IGroupToePortsViewProps,
  IToePortAttr,
  IToePortEdge,
  IToePortData,
  IToePortsConnection,
  IUpdateToePortResultAttr,
};
