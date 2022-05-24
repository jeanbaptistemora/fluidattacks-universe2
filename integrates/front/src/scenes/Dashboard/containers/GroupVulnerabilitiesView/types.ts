interface IFinding {
  id: string;
  title: string;
}

interface IGroupFindings {
  group: {
    findings: IFinding[];
    name: string;
  };
}

interface IVulnerabilityNode {
  id: string;
  where: string;
  specific: string;
}

interface IVulnerability extends IVulnerabilityNode {
  findings: IFinding[];
}

interface IFindingVulnerabilities {
  finding: {
    id: string;
    vulnerabilitiesConnection: {
      edges: { node: IVulnerabilityNode }[];
      pageInfo: {
        hasNextPage: boolean;
        endCursor: string;
      };
    };
  };
}

export type {
  IFinding,
  IFindingVulnerabilities,
  IGroupFindings,
  IVulnerability,
  IVulnerabilityNode,
};
