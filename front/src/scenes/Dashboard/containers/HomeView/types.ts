import { RouteComponentProps } from "react-router";
import { IDashboardState } from "../../reducer";

export type IHomeViewBaseProps = RouteComponentProps;

export interface IHomeViewStateProps {
  displayPreference: IDashboardState["user"]["displayPreference"];
}

export interface IHomeViewDispatchProps {
  onDisplayChange(value: IDashboardState["user"]["displayPreference"]): void;
}

export type IHomeViewProps = RouteComponentProps;

export interface IState { dashboard: IDashboardState; }

export interface IUserAttr {
  me: {
    projects: Array<{ description: string; name: string }>;
  };
}
