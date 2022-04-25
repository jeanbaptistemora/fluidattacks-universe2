interface IEventsDataset {
  group: {
    events: {
      eventStatus: string;
    }[];
  };
}

interface IGroupContext {
  path: string;
  url: string;
}

export type { IEventsDataset, IGroupContext };
