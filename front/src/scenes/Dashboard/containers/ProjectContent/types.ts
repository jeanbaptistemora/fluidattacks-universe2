import { RouteComponentProps } from "react-router";

export type IProjectContentBaseProps = Pick<RouteComponentProps<{ projectName: string }>, "match">;

export interface IProjectContentStateProps {
  userRole: string;
}

export interface IProjectContentDispatchProps {
  onLoad(): void;
}

export type IProjectContentProps = IProjectContentBaseProps &
  (IProjectContentStateProps & IProjectContentDispatchProps);
