interface IAddStakeholderAttr {
  addStakeholder: {
    email: string;
    success: boolean;
  };
}

interface IUser {
  me: {
    permissions: string[];
    userEmail: string;
    userName: string;
  };
}

interface ISessionExpirationAttr {
  me: {
    sessionExpiration: string;
  };
}

export { IAddStakeholderAttr, IUser, ISessionExpirationAttr };
