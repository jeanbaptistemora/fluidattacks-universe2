/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

interface IUpdateGroupResultAttr {
  updateSubscription?: {
    success: boolean;
  };
  updateGroupManaged?: {
    success: boolean;
  };
}

export type { IUpdateGroupResultAttr };
