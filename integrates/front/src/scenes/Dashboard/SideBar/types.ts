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
    };
  };
}

export type { IGroupData, IGetOrganizationGroups, IGroupTabVulns, INodeData };
