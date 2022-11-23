/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { IIPRootAttr, Root } from "./types";

const isIPRoot = (root: Root): root is IIPRootAttr =>
  root.__typename === "IPRoot";

const isActiveIPRoot = (root: IIPRootAttr): boolean => root.state === "ACTIVE";

export { isIPRoot, isActiveIPRoot };
