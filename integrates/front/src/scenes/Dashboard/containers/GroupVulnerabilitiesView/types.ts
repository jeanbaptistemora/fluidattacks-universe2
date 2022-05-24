interface IFinding {
  id: string;
  severityScore: number;
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
  reportDate: string;
  specific: string;
}

interface IVulnerability extends IVulnerabilityNode {
  finding: IFinding;
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
