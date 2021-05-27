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
      phoneNumber: string;
      responsibility: string;
      role: string;
    };
    success: boolean;
  };
}

interface IGetStakeholdersAttrs {
  project: {
    stakeholders: IStakeholderAttrs[];
  };
}

interface IStakeholderAttrs {
  email: string;
  firstLogin: string;
  lastLogin: string;
  organization: string;
  phoneNumber: string;
  projectName: string;
  responsibility: string;
  role: string;
}

interface IEditStakeholderAttr {
  editStakeholder: {
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
  IEditStakeholderAttr,
};
