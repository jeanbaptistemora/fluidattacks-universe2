export interface IAddUserAttr {
  addUser: {
    email: string;
    success: boolean;
  };
}

export interface IGetUserPermissionsAttr {
  me: {
    permissions: string[];
  };
}
