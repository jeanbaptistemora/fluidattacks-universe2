import { RouteComponentProps } from "react-router";

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

export interface IGetStakeholdersAttrs {
  project: {
    stakeholders: IStakeholderAttrs[];
  };
}

export interface IStakeholderAttrs {
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
    modifiedStakeholder: {
      email: string;
    };
    success: boolean;
  };
}

export type IProjectStakeholdersViewProps = RouteComponentProps<{ projectName: string }>;
