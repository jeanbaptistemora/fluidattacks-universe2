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

interface IVulnerability {
  currentState: string;
  finding: IFinding;
  id: string;
  reportDate: string;
  specific: string;
  treatment: string;
  where: string;
}

interface IFindingVulnerabilities {
  finding: {
    id: string;
    vulnerabilitiesConnection: {
      edges: { node: IVulnerability }[];
      pageInfo: {
        hasNextPage: boolean;
        endCursor: string;
      };
    };
  };
}

interface IGroupVulnerabilities {
  group: {
    name: string;
    vulnerabilities: {
      edges: { node: IVulnerability }[];
    };
  };
}

export type {
  IFinding,
  IFindingVulnerabilities,
  IGroupFindings,
  IGroupVulnerabilities,
  IVulnerability,
};
