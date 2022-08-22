interface IVulnerabilitiesLoaderProps {
  findingId: string;
  setFindingVulnerabilities: (
    setStateFn: (
      prevState: Record<string, IVulnerabilitiesResume>
    ) => Record<string, IVulnerabilitiesResume>
  ) => void;
}

interface IVulnerabilityAttr {
  id: string;
  treatmentAssigned: string | null;
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

interface IVulnerabilitiesResume {
  assignments: string;
  wheres: string;
}

interface IFindingAttr {
  id: string;
  vulnerabilitiesToReattackConnection: IVulnerabilitiesConnection;
}

export type {
  IFindingAttr,
  IVulnerabilityEdge,
  IVulnerabilitiesConnection,
  IVulnerabilitiesResume,
  IVulnerabilityAttr,
  IVulnerabilitiesLoaderProps,
};
