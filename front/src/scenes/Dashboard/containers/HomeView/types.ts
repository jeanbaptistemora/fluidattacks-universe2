import { RouteComponentProps } from "react-router";

export type IHomeViewProps = RouteComponentProps;

export interface ITagData {
  name: string;
  projects: Array<{ name: string }>;
}

export interface IUserAttr {
  me: {
    projects: Array<{ description: string; name: string }>;
    tags: ITagData[];
  };
}
