interface IAffectedReattacks {
  findingId: string;
  where: string;
  specific: string;
}

interface IEventDescriptionData {
  event: {
    accessibility: string[];
    affectedComponents: string[];
    affectedReattacks: IAffectedReattacks[];
    hacker: string;
    client: string;
    detail: string;
    eventStatus: string;
    id: string;
    otherSolvingReason: string | null;
    solvingReason: string | null;
  };
}

interface IUpdateEventSolvingReasonAttr {
  updateEventSolvingReason: {
    success: boolean;
  };
}

export type {
  IAffectedReattacks,
  IEventDescriptionData,
  IUpdateEventSolvingReasonAttr,
};
