interface IAddStakeholderAttr {
  addStakeholder: {
    email: string;
    success: boolean;
  };
}

interface IUser {
  me: {
    isConcurrentSession: boolean;
    permissions: string[];
    sessionExpiration: string;
    userEmail: string;
    userName: string;
  };
}

export { IAddStakeholderAttr, IUser };
