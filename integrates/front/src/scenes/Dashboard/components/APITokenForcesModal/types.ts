/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

interface IUpdateForcesTokenAttr {
  updateForcesAccessToken: {
    sessionJwt: string;
    success: boolean;
  };
}

interface IGetForcesTokenAttr {
  group: {
    forcesToken: string | undefined;
  };
}

export type { IUpdateForcesTokenAttr, IGetForcesTokenAttr };
