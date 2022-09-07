/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { IGitRootAttr, IIPRootAttr, IURLRootAttr, Root } from "./types";

const isGitRoot = (root: Root): root is IGitRootAttr =>
  root.__typename === "GitRoot";

const isIPRoot = (root: Root): root is IIPRootAttr =>
  root.__typename === "IPRoot";

const isURLRoot = (root: Root): root is IURLRootAttr =>
  root.__typename === "URLRoot";

function mapInactiveStatus(roots: IGitRootAttr[]): IGitRootAttr[] {
  return roots.map((root: IGitRootAttr): IGitRootAttr => {
    if (root.state === "INACTIVE") {
      return {
        ...root,
        cloningStatus: { message: root.cloningStatus.message, status: "N/A" },
      };
    }

    return root;
  });
}

export { isGitRoot, isIPRoot, isURLRoot, mapInactiveStatus };
