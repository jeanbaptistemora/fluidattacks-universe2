import { RouteComponentProps } from "react-router";

export type IFindingContentProps = RouteComponentProps<{ findingId: string; projectName: string }>;

export interface IHeaderQueryResult {
  finding: {
    analyst?: string;
    closedVulns: number;
    historicState: Array<{
      analyst: string; date: string; state: string;
    }>;
    id: string;
    openVulns: number;
    releaseDate: string;
    reportDate: string;
    severityScore: number;
    state: "open" | "closed" | "default";
    title: string;
  };
}
