/**
 * Organization attributes
 */
interface IOrganization {
  analytics: {
    current: {
      closed: number;
      open: number;
    };
    previous: {
      closed: number;
      open: number;
    };
    totalGroups: number;
  };
  name: string;
}

/**
 * Query data response type
 */
interface IOrgsResult {
  me: {
    organizations: IOrganization[];
  };
}

export type { IOrganization, IOrgsResult };
