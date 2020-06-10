/**
 * Project attributes
 */
export interface IProject {
  closedVulnerabilities: number;
  isCommunity: boolean;
  openVulnerabilities: number;
  serviceAttributes?: string[];
}

/**
 * Query data response type
 */
export interface IProjectsResult {
  me: {
    projects: IProject[];
  };
}
