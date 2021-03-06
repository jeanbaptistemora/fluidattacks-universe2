interface IAddStakeholderAttrs {
  grantStakeholderOrganizationAccess: {
    grantedStakeholder: {
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

interface IEditStakeholderAttrs {
  editStakeholderOrganization: {
    modifiedStakeholder: {
      email: string;
    };
    success: boolean;
  };
}

interface IOrganizationStakeholders {
  organizationId: string;
}

interface IRemoveStakeholderAttrs {
  removeStakeholderOrganizationAccess: {
    success: boolean;
  };
}

interface ILastLogin {
  label: string;
  value: number[];
}

interface IStakeholderAttrs {
  email: string;
  firstLogin: string;
  lastLogin: ILastLogin;
  organization: string;
  phoneNumber: string;
  responsibility: string;
  role: string;
}

export {
  IAddStakeholderAttrs,
  IEditStakeholderAttrs,
  IOrganizationStakeholders,
  IRemoveStakeholderAttrs,
  IStakeholderAttrs,
};
