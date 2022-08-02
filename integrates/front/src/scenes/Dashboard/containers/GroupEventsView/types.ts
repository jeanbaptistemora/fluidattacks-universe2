interface IRootAttr {
  id: string;
  nickname: string;
}

interface IEventAttr {
  accessibility: string[];
  affectedComponents: string[];
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
  accessibility: string;
  affectedComponents: string;
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
  accessibility: string;
  afectComps: string;
  closingDateRange: { max: string; min: string };
  dateRange: { max: string; min: string };
  status: string;
  type: string;
}

export type { IEventAttr, IEventData, IEventsDataset, IFilterSet };
