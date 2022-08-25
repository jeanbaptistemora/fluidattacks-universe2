interface IAddEventResultAttr {
  addEvent: {
    eventId: string;
    success: boolean;
  };
}

interface IRootAttr {
  id: string;
  nickname: string;
}

interface IEventAttr {
  closingDate: string;
  detail: string;
  eventDate: string;
  eventStatus: string;
  eventType: string;
  id: string;
  groupName: string;
  root: IRootAttr | null;
}

interface IEventData {
  closingDate: string;
  detail: string;
  eventDate: string;
  eventStatus: string;
  eventType: string;
  id: string;
  groupName: string;
  root: IRootAttr | null;
}

interface IEventsDataset {
  group: {
    events: IEventAttr[];
  };
}

interface IFilterSet {
  closingDateRange: { max: string; min: string };
  dateRange: { max: string; min: string };
  status: string;
  type: string;
}

interface IRequestEventVerificationResultAttr {
  requestEventVerification: {
    success: boolean;
  };
}

export type {
  IAddEventResultAttr,
  IEventAttr,
  IEventData,
  IEventsDataset,
  IFilterSet,
  IRequestEventVerificationResultAttr,
};
