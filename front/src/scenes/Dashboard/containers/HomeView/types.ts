import { RouteComponentProps } from "react-router";

export type IHomeViewProps = RouteComponentProps;

export interface IUserAttr {
  me: {
    projects: Array<{ description: string; name: string }>;
  };
}
