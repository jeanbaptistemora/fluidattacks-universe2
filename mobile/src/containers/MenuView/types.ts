/**
 * Project attributes
 */
export interface IProject {
  description: string;
  name: string;
}

/**
 * Query data response type
 */
export interface IProjectsResult {
  me: {
    projects: IProject[];
  };
}
