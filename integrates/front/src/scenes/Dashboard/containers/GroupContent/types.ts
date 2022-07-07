interface IGetEventStatus {
  group: {
    events: {
      eventStatus: string;
    }[];
    name: string;
  };
}

interface IGroupContext {
  path: string;
  url: string;
}

export type { IGetEventStatus, IGroupContext };
