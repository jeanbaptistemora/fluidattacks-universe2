import { QueryResult } from "react-apollo";
import { RouteComponentProps } from "react-router-native";

export type IMenuProps = RouteComponentProps;

/**
 * Project attributes retrieved from api
 */
export interface IProject {
  description: string;
  name: string;
}

export type PROJECTS_RESULT = QueryResult<{
  me: {
    projects: IProject[];
  };
}>;
