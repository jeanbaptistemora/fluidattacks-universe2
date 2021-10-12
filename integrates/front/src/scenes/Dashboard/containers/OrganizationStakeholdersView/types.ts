interface IAddStakeholderAttrs {
  grantStakeholderOrganizationAccess: {
    grantedStakeholder: {
      email: string;
      firstLogin: string;
      lastLogin: string;
      role: string;
      userOrganization: string;
    };
    success: boolean;
  };
}

interface IUpdateStakeholderAttrs {
  updateOrganizationStakeholder: {
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
  responsibility: string;
  role: string;
}

export {
  IAddStakeholderAttrs,
  IUpdateStakeholderAttrs,
  IOrganizationStakeholders,
  IRemoveStakeholderAttrs,
  IStakeholderAttrs,
};
