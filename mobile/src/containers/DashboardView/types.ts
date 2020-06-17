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
 * Query data response type
 */
export interface IGroupsResult {
  me: {
    groups: IGroup[];
  };
}
