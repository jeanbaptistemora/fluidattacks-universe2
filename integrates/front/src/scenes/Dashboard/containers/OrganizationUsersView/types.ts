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

export interface IEditStakeholderAttrs {
  editStakeholderOrganization: {
    modifiedStakeholder: {
      email: string;
    };
    success: boolean;
  };
 }

export interface IOrganizationUsers {
  organizationId: string;
}

export interface IRemoveStakeholderAttrs {
  removeStakeholderOrganizationAccess: {
    success: boolean;
  };
}

export interface ILastLogin {
  label: string;
  value: number[];
}

export interface IStakeholderAttrs {
  email: string;
  firstLogin: string;
  lastLogin: ILastLogin;
  organization: string;
  phoneNumber: string;
  responsibility: string;
  role: string;
}
