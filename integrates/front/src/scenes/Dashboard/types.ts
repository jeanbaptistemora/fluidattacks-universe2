interface IAddStakeholderAttr {
  addStakeholder: {
    email: string;
    success: boolean;
  };
}

interface IGetUserPermissionsAttr {
  me: {
    permissions: string[];
  };
}

export { IAddStakeholderAttr, IGetUserPermissionsAttr };
