interface ITodoFindingToReattackAttr {
  groupName: string;
  id: string;
  title: string;
  vulnerabilitiesToReattackConnection: IVulnerabilitiesConnection;
  verificationSummary: {
    requested: string;
  };
}

interface IFindingToReattackEdge {
  node: ITodoFindingToReattackAttr;
}

interface IFindingToReattackConnection {
  edges: IFindingToReattackEdge[];
  pageInfo: {
    endCursor: string;
    hasNextPage: boolean;
  };
  total: number | undefined;
}

interface IGetTodoReattacks {
  me: {
    findingReattacks: ITodoFindingToReattackAttr[];
  };
}

interface IVulnerabilityAttr {
  id: string;
  lastRequestedReattackDate: string;
}

interface IVulnerabilityEdge {
  node: IVulnerabilityAttr;
}

interface IVulnerabilitiesConnection {
  edges: IVulnerabilityEdge[];
  pageInfo: {
    endCursor: string;
    hasNextPage: boolean;
  };
  total: number | undefined;
}
interface IFindingFormatted extends ITodoFindingToReattackAttr {
  oldestReattackRequestedDate: string;
  url: string;
}

export type {
  IFindingFormatted,
  IFindingToReattackConnection,
  IFindingToReattackEdge,
  IGetTodoReattacks,
  ITodoFindingToReattackAttr,
  IVulnerabilityAttr,
  IVulnerabilityEdge,
};
