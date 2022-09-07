/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { createContext } from "react";

import type { IAssignedVulnerabilitiesContext } from "scenes/Dashboard/types";

export const AssignedVulnerabilitiesContext =
  createContext<IAssignedVulnerabilitiesContext>([[], (): void => undefined]);
