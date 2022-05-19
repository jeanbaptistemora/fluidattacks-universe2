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

interface IVulnerability {
  id: string;
  where: string;
  specific: string;
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

export type {
  IFinding,
  IFindingVulnerabilities,
  IGroupFindings,
  IVulnerability,
};
