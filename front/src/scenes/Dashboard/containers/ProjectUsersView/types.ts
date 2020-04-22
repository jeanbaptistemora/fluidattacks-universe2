import { RouteComponentProps } from "react-router";

export interface IUsersAttr {
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

export type IProjectUsersViewProps = RouteComponentProps<{ projectName: string }>;
