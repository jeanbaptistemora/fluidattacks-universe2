interface IGroupData {
  name: string;
}

interface INodeData {
  node: {
    currentState: string;
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
    vulnerabilities: {
      edges: INodeData[];
    };
  };
}

export type { IGroupData, IGetOrganizationGroups, IGroupTabVulns, INodeData };
