interface IHeaderQueryResult {
  finding: {
    closedVulns: number;
    currentState: string;
    hacker?: string;
    id: string;
    minTimeToRemediate: number;
    openVulns: number;
    releaseDate: string | null;
    severityScore: number;
    status: "SAFE" | "VULNERABLE";
    title: string;
  };
}

interface IRemoveFindingResultAttr {
  removeFinding?: {
    success: boolean;
  };
}

export type { IHeaderQueryResult, IRemoveFindingResultAttr };
