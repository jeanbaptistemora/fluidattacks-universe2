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
    closingDate: string;
    hacker: string;
    client: string;
    detail: string;
    eventType: string;
    eventStatus: string;
    id: string;
    otherSolvingReason: string | null;
    solvingReason: string | null;
  };
}

interface IDescriptionFormValues {
  affectedComponents: string[];
  eventType: string;
  otherSolvingReason: string | null;
  solvingReason: string | null;
}

interface IUpdateEventAttr {
  updateEvent: {
    success: boolean;
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
  IDescriptionFormValues,
  IUpdateEventAttr,
  IUpdateEventSolvingReasonAttr,
};
