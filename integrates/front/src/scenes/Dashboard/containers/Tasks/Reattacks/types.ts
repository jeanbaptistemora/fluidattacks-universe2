interface ITodoFindingToReattackAttr {
  age: number;
  currentState: string;
  groupName: string;
  hacker: string;
  id: string;
  lastVulnerability: number;
  openVulnerabilities: number;
  severityScore: number;
  state: string;
  title: string;
  vulnerabilitiesToReattackConnection: IVulnerabilitiesConnection;
}

interface ITodoGroupAttr {
  findings: ITodoFindingToReattackAttr[];
}

interface ITodoOrganizationAttr {
  groups: ITodoGroupAttr[];
  name: string;
}

interface IGetTodoReattacks {
  me: {
    organizations: ITodoOrganizationAttr[];
  };
}

interface IVulnerabilityAttr {
  id: string;
  lastRequestedReattackDate: string;
}

interface IVulnerabilityEdge {
  node: IVulnerabilityAttr;
}

interface IVulnerabilitiesConnection {
  edges: IVulnerabilityEdge[];
}
interface IFindingFormatted extends ITodoFindingToReattackAttr {
  oldestReattackRequestedDate: string;
}

export type {
  IGetTodoReattacks,
  IFindingFormatted,
  ITodoFindingToReattackAttr,
  ITodoGroupAttr,
  ITodoOrganizationAttr,
  IVulnerabilityAttr,
  IVulnerabilityEdge,
};
