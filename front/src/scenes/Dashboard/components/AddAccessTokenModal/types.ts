export interface IInvalidateAccessTokenAttr {
  invalidateAccessToken: {
    success: boolean;
  };
}

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
    accessToken: string;
  };
}

export interface IGetAccessTokenDictAttr {
  hasAccessToken: boolean;
  issuedAt: number;
}
