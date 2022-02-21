interface IFilterSet {
  bePresent: string;
  component: string;
  hasVulnerabilities: string;
  root: string;
  seenAt: { max: string; min: string };
}

interface IGroupToeInputsViewProps {
  isInternal: boolean;
}

interface IRemoveToeInputResultAttr {
  removeToeInput: {
    success: boolean;
  };
}

interface IToeInputEdge {
  node: IToeInputAttr;
}

interface IToeInputsConnection {
  edges: IToeInputEdge[];
  pageInfo: {
    hasNextPage: boolean;
    endCursor: string;
  };
}
interface IToeInputAttr {
  attackedAt: string | null;
  attackedBy: string;
  bePresent: boolean;
  bePresentUntil: string | null;
  component: string;
  entryPoint: string;
  firstAttackAt: string | null;
  hasVulnerabilities: boolean;
  seenAt: string | null;
  seenFirstTimeBy: string;
  unreliableRootNickname: string;
}

interface IToeInputData {
  attackedAt: Date | undefined;
  attackedBy: string;
  bePresent: boolean;
  bePresentUntil: Date | undefined;
  component: string;
  entryPoint: string;
  firstAttackAt: Date | undefined;
  hasVulnerabilities: boolean;
  markedRootNickname: string;
  seenAt: Date | undefined;
  seenFirstTimeBy: string;
  unreliableRootNickname: string;
}

export type {
  IFilterSet,
  IGroupToeInputsViewProps,
  IRemoveToeInputResultAttr,
  IToeInputAttr,
  IToeInputEdge,
  IToeInputData,
  IToeInputsConnection,
};
