interface IGroupData {
  name: string;
}

interface INodeData {
  node: {
    state: string;
    zeroRisk: string;
  };
}

interface IGetOrganizationGroups {
  organizationId: {
    groups: IGroupData[];
  };
}

interface IGroupTabVulns {
  group: {
    name: string;
    vulnerabilities: {
      edges: INodeData[];
      pageInfo: {
        endCursor: string;
        hasNextPage: boolean;
      };
      total: number | undefined;
    };
  };
}

export type { IGroupData, IGetOrganizationGroups, IGroupTabVulns, INodeData };
