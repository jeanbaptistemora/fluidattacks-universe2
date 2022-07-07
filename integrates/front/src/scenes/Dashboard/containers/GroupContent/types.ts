interface IEventDataset {
  eventDate: string;
  eventStatus: string;
  groupName: string;
}

interface IEventBarDataset {
  organizationId: {
    groups: {
      events: IEventDataset[];
      name: string;
    }[];
    name: string;
  };
}

interface IGroupContext {
  path: string;
  url: string;
}

export type { IEventBarDataset, IEventDataset, IGroupContext };
