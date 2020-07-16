/**
 * Organization attributes
 */
export interface IOrganization {
  analytics: {
    current: {
      closed: number;
      open: number;
    };
    previous: {
      closed: number;
      open: number;
    };
  };
  totalGroups: number;
}

/**
 * Query data response type
 */
export interface IOrgsResult {
  me: {
    organizations: IOrganization[];
  };
}
