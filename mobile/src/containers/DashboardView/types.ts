/**
 * Project attributes
 */
export interface IProject {
  closedVulnerabilities: number;
  openVulnerabilities: number;
}

/**
 * Query data response type
 */
export interface IProjectsResult {
  me: {
    projects: IProject[];
  };
}
