/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { createContext } from "react";

import type { ICommentContext } from "./types";

export const commentContext: React.Context<ICommentContext> = createContext({
  replying: 0,
});
