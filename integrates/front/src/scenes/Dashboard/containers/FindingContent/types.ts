interface IHeaderQueryResult {
  finding: {
    closedVulns: number;
    currentState: string;
    hacker?: string;
    historicState: {
      analyst: string;
      date: string;
      state: string;
    }[];
    id: string;
    minTimeToRemediate: number;
    openVulns: number;
    releaseDate: string | null;
    severityScore: number;
    state: "closed" | "default" | "open";
    title: string;
  };
}

interface IRemoveFindingResultAttr {
  removeFinding?: {
    success: boolean;
  };
}

export type { IHeaderQueryResult, IRemoveFindingResultAttr };
