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

export type { IFinding, IGroupFindings };
