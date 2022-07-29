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

interface IGroupPermissions {
  name: string;
  permissions: string[];
  userRole: string;
}

export type { IGetEventStatus, IGroupContext, IGroupPermissions };
