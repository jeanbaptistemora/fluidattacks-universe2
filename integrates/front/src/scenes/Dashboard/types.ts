export interface IAddStakeholderAttr {
  addStakeholder: {
    email: string;
    success: boolean;
  };
}

export interface IGetUserPermissionsAttr {
  me: {
    permissions: string[];
  };
}
