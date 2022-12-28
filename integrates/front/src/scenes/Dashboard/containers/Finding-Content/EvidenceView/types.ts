interface IGetFindingEvidences {
  finding: {
    evidence: {
      animation: {
        date: string | null;
        description: string | null;
        url: string | null;
      };
      evidence1: {
        date: string | null;
        description: string | null;
        url: string | null;
      };
      evidence2: {
        date: string | null;
        description: string | null;
        url: string | null;
      };
      evidence3: {
        date: string | null;
        description: string | null;
        url: string | null;
      };
      evidence4: {
        date: string | null;
        description: string | null;
        url: string | null;
      };
      evidence5: {
        date: string | null;
        description: string | null;
        url: string | null;
      };
      exploitation: {
        date: string | null;
        description: string | null;
        url: string | null;
      };
    };
    id: string;
  };
}

interface IEvidenceItem {
  date?: string;
  description: string;
  url: string;
}

export type { IGetFindingEvidences, IEvidenceItem };
