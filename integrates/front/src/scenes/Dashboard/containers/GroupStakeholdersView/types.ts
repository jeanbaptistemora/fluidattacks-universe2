interface IRemoveStakeholderAttr {
  removeStakeholderAccess: {
    removedEmail: string;
    success: boolean;
  };
}

interface IAddStakeholderAttr {
  grantStakeholderAccess: {
    grantedStakeholder: {
      email: string;
      firstLogin: string;
      lastLogin: string;
      organization: string;
      responsibility: string;
      role: string;
    };
    success: boolean;
  };
}

interface IGetStakeholdersAttrs {
  group: {
    stakeholders: IStakeholderAttrs[];
  };
}

interface IStakeholderDataSet {
  email: string;
  firstLogin: string;
  invitationState: string;
  lastLogin: string;
  organization: string;
  groupName: string;
  responsibility: string;
  role: string;
  invitationResend: JSX.Element;
}

interface IStakeholderAttrs {
  email: string;
  firstLogin: string;
  invitationState: string;
  lastLogin: string;
  organization: string;
  groupName: string;
  responsibility: string;
  role: string;
}

interface IUpdateGroupStakeholderAttr {
  updateGroupStakeholder: {
    modifiedStakeholder: {
      email: string;
    };
    success: boolean;
  };
}

export {
  IRemoveStakeholderAttr,
  IAddStakeholderAttr,
  IGetStakeholdersAttrs,
  IStakeholderAttrs,
  IStakeholderDataSet,
  IUpdateGroupStakeholderAttr,
};
