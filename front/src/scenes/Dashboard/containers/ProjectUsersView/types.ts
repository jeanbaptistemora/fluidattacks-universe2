import { RouteComponentProps } from "react-router";
import { IDashboardState } from "../../reducer";

export interface IUsersAttr {
  me: {
    role: string;
  };
  project: {
    users: Array<{
      email: string;
      firstLogin: string;
      lastLogin: string;
      organization: string;
      phoneNumber: string;
      responsibility: string;
      role: string;
    }>;
  };
}

export interface IRemoveUserAttr {
  removeUserAccess: {
    removedEmail: string;
    success: boolean;
  };
}

export interface IAddUserAttr {
  grantUserAccess: {
    grantedUser: {
      email: string;
      firstLogin: string;
      lastLogin: string;
      organization: string;
      phoneNumber: string;
      responsibility: string;
      role: string;
    };
    success: boolean;
  };
}

export interface IUserDataAttr {
  email: string;
  firstLogin: string;
  lastLogin: string;
  organization: string;
  phoneNumber: string;
  projectName: string;
  responsibility: string;
  role: string;
}

export interface IEditUserAttr {
  editUser: {
    success: boolean;
  };
}

export type IProjectUsersBaseProps = Pick<RouteComponentProps<{ projectName: string }>, "match">;

export type IProjectUsersStateProps = IDashboardState["users"] & {
  userRole: string;
};

export interface IProjectUsersDispatchProps {
  onCloseUsersModal(): void;
  onOpenModal(type: "add" | "edit", initialValues?: {}): void;
}

export type IProjectUsersViewProps = IProjectUsersBaseProps & (IProjectUsersStateProps & IProjectUsersDispatchProps);

export interface IState { dashboard: IDashboardState; }
