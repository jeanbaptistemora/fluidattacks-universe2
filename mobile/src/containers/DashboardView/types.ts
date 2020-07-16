/**
 * Group attributes
 */
export interface IGroup {
  closedVulnerabilities: number;
  isCommunity: boolean;
  openVulnerabilities: number;
  serviceAttributes?: string[];
}

/**
 * Organization attributes
 */
export interface IOrganization {
  analytics: {
    current: {
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
    groups: IGroup[];
    organizations: IOrganization[];
  };
}
