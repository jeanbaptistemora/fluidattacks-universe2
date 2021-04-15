export interface IHeaderQueryResult {
  finding: {
    analyst?: string;
    closedVulns: number;
    historicState: {
      analyst: string;
      date: string;
      state: string;
    }[];
    id: string;
    openVulns: number;
    releaseDate: string;
    severityScore: number;
    state: "closed" | "default" | "open";
    title: string;
  };
}
