/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

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
}

export type {
  IInvalidateAccessTokenAttr,
  IUpdateAccessTokenAttr,
  IAccessTokenAttr,
  IGetAccessTokenAttr,
  IGetAccessTokenDictAttr,
};
