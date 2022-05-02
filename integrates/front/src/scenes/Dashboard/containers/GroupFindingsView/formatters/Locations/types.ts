interface ILocationsProps {
  findingId: string;
  setFindingLocations: (
    setStateFn: (prevState: Record<string, string>) => Record<string, string>
  ) => void;
}

interface IVulnerabilityAttr {
  id: string;
  where: string;
}

interface IVulnerabilityEdge {
  node: IVulnerabilityAttr;
}

interface IVulnerabilitiesConnection {
  edges: IVulnerabilityEdge[];
  pageInfo: {
    hasNextPage: boolean;
    endCursor: string;
  };
}

interface IFindingAttr {
  id: string;
  vulnerabilitiesToReattackConnection: IVulnerabilitiesConnection;
}

export type {
  IFindingAttr,
  IVulnerabilityEdge,
  IVulnerabilitiesConnection,
  IVulnerabilityAttr,
  ILocationsProps,
};
