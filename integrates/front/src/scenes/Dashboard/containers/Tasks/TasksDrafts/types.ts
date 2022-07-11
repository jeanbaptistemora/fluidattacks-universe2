interface ITodoDraftAttr {
  currentState: string;
  groupName: string;
  hacker: string;
  id: string;
  openVulnerabilities: number;
  reportDate: string | null;
  severityScore: number;
  title: string;
}

interface ITodoGroupAttr {
  drafts: ITodoDraftAttr[];
}

interface ITodoOrganizationAttr {
  groups: ITodoGroupAttr[];
}

interface IGetTodoDrafts {
  me: {
    organizations: ITodoOrganizationAttr[];
  };
}

export type {
  IGetTodoDrafts,
  ITodoDraftAttr,
  ITodoGroupAttr,
  ITodoOrganizationAttr,
};
