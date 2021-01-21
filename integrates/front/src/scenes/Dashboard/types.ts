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

interface ISessionExpirationAttr {
  me: {
    sessionExpiration: string;
  };
}

export { IAddStakeholderAttr, IGetUserPermissionsAttr, ISessionExpirationAttr };
