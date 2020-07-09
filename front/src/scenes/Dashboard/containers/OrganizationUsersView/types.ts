export interface IAddUserAttrs {
  grantUserOrganizationAccess: {
    grantedUser: {
      email: string;
      firstLogin: string;
      lastLogin: string;
      phoneNumber: string;
      role: string;
      userOrganization: string;
    };
    success: boolean;
  };
}

export interface IEditUserAttrs {
  editUserOrganization: {
    modifiedUser: {
      email: string;
    };
    success: boolean;
  };
 }

export interface IOrganizationUsers {
  organizationId: string;
}

export interface IRemoveUserAttrs {
  removeUserOrganizationAccess: {
    success: boolean;
  };
}

export interface ILastLogin {
  label: string;
  value: number[];
}

export interface IUserAttrs {
  email: string;
  firstLogin: string;
  lastLogin: ILastLogin;
  organization: string;
  phoneNumber: string;
  responsibility: string;
  role: string;
}
