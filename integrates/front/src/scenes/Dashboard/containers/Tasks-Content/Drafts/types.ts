interface ITodoDraftAttr {
  currentState: string;
  groupName: string;
  hacker: string;
  id: string;
  openVulnerabilities: number;
  organizationName: string | undefined;
  lastStateDate: string;
  reportDate: string | null;
  severityScore: number;
  title: string;
}

interface IGetTodoDrafts {
  me: {
    drafts: ITodoDraftAttr[];
  };
}

export type { IGetTodoDrafts, ITodoDraftAttr };
