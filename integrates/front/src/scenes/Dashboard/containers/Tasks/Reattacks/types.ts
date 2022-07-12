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

export type {
  IGetTodoReattacks,
  ITodoFindingToReattackAttr,
  ITodoGroupAttr,
  ITodoOrganizationAttr,
};
