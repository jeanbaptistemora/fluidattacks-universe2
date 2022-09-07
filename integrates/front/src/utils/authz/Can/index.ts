/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { PureAbility } from "@casl/ability";
import type { BoundCanProps } from "@casl/react";
import { createContextualCan } from "@casl/react";
import type React from "react";

import { authzPermissionsContext } from "utils/authz/config";

const can: React.FC<BoundCanProps<PureAbility<string>>> = createContextualCan(
  authzPermissionsContext.Consumer
);

export { can as Can };
