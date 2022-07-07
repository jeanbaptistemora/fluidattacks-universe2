interface IEventDataset {
  eventDate: string;
  eventStatus: string;
  groupName: string;
}

interface IEventBarDataset {
  organizationId: {
    id: string;
    groups: {
      events: IEventDataset[];
      name: string;
    }[];
    name: string;
  };
}

interface IEventBarProps {
  organizationName: string;
}

export type { IEventDataset, IEventBarDataset, IEventBarProps };
