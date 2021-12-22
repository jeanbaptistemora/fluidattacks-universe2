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
  attackedAt: string;
  attackedBy: string;
  bePresent: boolean;
  bePresentUntil: string;
  component: string;
  entryPoint: string;
  firstAttackAt: string;
  seenAt: string;
  seenFirstTimeBy: string;
  unreliableRootNickname: string;
}

interface IToeInputData {
  attackedAt: string;
  attackedBy: string;
  bePresent: boolean;
  bePresentUntil: string;
  component: string;
  entryPoint: string;
  firstAttackAt: string;
  seenAt: string;
  seenFirstTimeBy: string;
  unreliableRootNickname: string;
}

export type {
  IToeInputAttr,
  IToeInputEdge,
  IToeInputData,
  IToeInputsConnection,
};
