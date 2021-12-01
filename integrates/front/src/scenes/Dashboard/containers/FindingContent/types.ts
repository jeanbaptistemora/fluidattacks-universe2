interface IHeaderQueryResult {
  finding: {
    closedVulns: number;
    hacker?: string;
    historicState: {
      analyst: string;
      date: string;
      state: string;
    }[];
    id: string;
    openVulns: number;
    releaseDate?: string;
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

export { IHeaderQueryResult, IRemoveFindingResultAttr };
