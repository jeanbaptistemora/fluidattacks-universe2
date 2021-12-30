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
  seenAt: Date | undefined;
  seenFirstTimeBy: string;
  unreliableRootNickname: string;
}

export type {
  IToeInputAttr,
  IToeInputEdge,
  IToeInputData,
  IToeInputsConnection,
};
