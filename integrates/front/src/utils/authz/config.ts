/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { PureAbility } from "@casl/ability";
import type React from "react";
import { createContext } from "react";

const groupAttributes: PureAbility<string> = new PureAbility<string>();
const groupLevelPermissions: PureAbility<string> = new PureAbility<string>();
const organizationLevelPermissions: PureAbility<string> =
  new PureAbility<string>();
const userLevelPermissions: PureAbility<string> = new PureAbility<string>();

const authzPermissionsContext = createContext(
  new PureAbility<string, unknown>()
);

const authzGroupContext: React.Context<PureAbility<string>> = createContext(
  new PureAbility<string>()
);

export {
  groupAttributes,
  groupLevelPermissions,
  organizationLevelPermissions,
  userLevelPermissions,
  authzPermissionsContext,
  authzGroupContext,
};
