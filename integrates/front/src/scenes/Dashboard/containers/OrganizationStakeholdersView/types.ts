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

interface IGetOrganizationStakeholders {
  organization: {
    name: string;
    stakeholders: IStakeholderAttrs[];
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
  invitationState: string;
  lastLogin: ILastLogin;
  role: string;
}

interface IStakeholderDataSet {
  email: string;
  firstLogin: string;
  invitationResend: JSX.Element;
  invitationState: string;
  lastLogin: ILastLogin;
  role: string;
}

export {
  IAddStakeholderAttrs,
  IGetOrganizationStakeholders,
  IUpdateStakeholderAttrs,
  IOrganizationStakeholders,
  IRemoveStakeholderAttrs,
  IStakeholderAttrs,
  IStakeholderDataSet,
};
