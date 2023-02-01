interface IInvalidateAccessTokenAttr {
  invalidateAccessToken: {
    success: boolean;
  };
}

interface IUpdateAccessTokenAttr {
  updateAccessToken: {
    sessionJwt: string;
    success: boolean;
  };
}

interface IAccessTokenAttr {
  expirationTime: string;
}

interface IGetAccessTokenAttr {
  me: {
    accessToken: string;
  };
}

interface IGetAccessTokenDictAttr {
  hasAccessToken: boolean;
  issuedAt: string;
  lastAccessTokenUse: string | null | undefined;
}

export type {
  IInvalidateAccessTokenAttr,
  IUpdateAccessTokenAttr,
  IAccessTokenAttr,
  IGetAccessTokenAttr,
  IGetAccessTokenDictAttr,
};
