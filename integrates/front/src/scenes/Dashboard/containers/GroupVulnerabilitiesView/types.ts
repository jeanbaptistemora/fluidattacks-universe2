interface IFinding {
  id: string;
  severityScore: number;
  title: string;
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

interface IGroupVulnerabilities {
  group: {
    name: string;
    vulnerabilities: {
      edges: { node: IVulnerability }[];
    };
  };
}

export type { IFinding, IGroupVulnerabilities, IVulnerability };
