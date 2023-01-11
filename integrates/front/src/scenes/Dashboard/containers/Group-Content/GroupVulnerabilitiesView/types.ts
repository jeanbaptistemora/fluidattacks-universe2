import type { IVulnRowAttr as IVulnerabilityAttr } from "scenes/Dashboard/components/Vulnerabilities/types";

interface IFinding {
  id: string;
  severityScore: number;
  title: string;
}

interface IGroupVulnerabilities {
  group: {
    name: string;
    vulnerabilities: {
      edges: { node: IVulnerabilityAttr }[];
      pageInfo: {
        endCursor: string;
        hasNextPage: boolean;
      };
      total: number | undefined;
    };
  };
}

export type { IFinding, IGroupVulnerabilities };
