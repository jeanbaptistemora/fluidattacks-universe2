import { RouteComponentProps } from "react-router";

export interface ILastLogin {
  label: string;
  value: number[];
}

export interface IStakeholderAttr {
  project: {
    stakeholders: Array<{
      email: string;
      firstLogin: string;
      lastLogin: ILastLogin;
      organization: string;
      phoneNumber: string;
      responsibility: string;
      role: string;
    }>;
  };
}

export interface IRemoveStakeholderAttr {
  removeStakeholderAccess: {
    removedEmail: string;
    success: boolean;
  };
}

export interface IAddStakeholderAttr {
  grantStakeholderAccess: {
    grantedStakeholder: {
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

export interface IStakeholderDataAttr {
  email: string;
  firstLogin: string;
  lastLogin: string;
  organization: string;
  phoneNumber: string;
  projectName: string;
  responsibility: string;
  role: string;
}

export interface IEditStakeholderAttr {
  editStakeholder: {
    success: boolean;
  };
}

export type IProjectStakeholdersViewProps = RouteComponentProps<{ projectName: string }>;
