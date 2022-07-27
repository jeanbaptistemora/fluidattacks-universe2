interface IGetEventStatus {
  group: {
    events: {
      eventStatus: string;
    }[];
    name: string;
  };
}

interface IGroupContext {
  organizationId: string;
  path: string;
  url: string;
}

export type { IGetEventStatus, IGroupContext };
