import type { IHistoricTreatment } from "../../Finding-Content/DescriptionView/types";
import type { IVulnRowAttr as IVulnerabilityAttr } from "scenes/Dashboard/components/Vulnerabilities/types";

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
  verification: string;
  where: string;
}

interface IVulnerabilitiesHistoricResume {
  historicTreatment: IHistoricTreatment[];
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

export type {
  IFinding,
  IGroupVulnerabilities,
  IVulnerabilitiesHistoricResume,
  IVulnerability,
};
