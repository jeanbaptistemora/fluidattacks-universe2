export interface IUpdateAccessTokenAttr {
  updateAccessToken: {
    sessionJwt: string;
    success: boolean;
  };
}

export interface IAccessTokenAttr {
  expirationTime: string;
}

export interface IGetAccessTokenAttr {
  me: {
    accessToken: boolean;
  };
}
