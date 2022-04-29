import type { IFinding } from "../types";

interface IVulnerabilitiesToReattackTableProps {
  finding: IFinding;
}

interface IVulnerabilityAttr {
  findingId: string;
  id: string;
  where: string;
  specific: string;
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
  IVulnerabilitiesToReattackTableProps,
};
