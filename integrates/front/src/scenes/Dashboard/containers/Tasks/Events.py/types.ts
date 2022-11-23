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

interface ITodoEvents {
  me: {
    pendingEvents: IEventAttr[];
    userEmail: string;
  };
}

export type { IEventAttr, ITodoEvents };
