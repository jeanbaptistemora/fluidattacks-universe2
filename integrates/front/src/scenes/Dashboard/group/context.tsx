/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { createContext } from "react";

import type { IGroupContext } from "./types";

const groupContext: React.Context<IGroupContext> = createContext({
  organizationId: "",
  path: "",
  url: "",
});

export { groupContext };
