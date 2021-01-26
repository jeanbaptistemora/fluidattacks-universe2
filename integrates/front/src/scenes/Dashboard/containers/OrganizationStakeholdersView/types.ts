export interface IAddStakeholderAttrs {
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

export interface IEditStakeholderAttrs {
  editStakeholderOrganization: {
    modifiedStakeholder: {
      email: string;
    };
    success: boolean;
  };
 }

export interface IGetStakeholdersAttrs {
  organization: {
    __typename: "Organization";
    stakeholders: {
      __typename: "GetStakeholdersPayload";
      numPages: number;
      stakeholders: IStakeholderAttrs[];
    };
  };
}

export interface IOrganizationStakeholders {
  organizationId: string;
  pageIndex?: number;
  pageSize?: number;
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
