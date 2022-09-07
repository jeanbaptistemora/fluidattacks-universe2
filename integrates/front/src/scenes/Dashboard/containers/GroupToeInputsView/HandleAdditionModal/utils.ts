/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import _ from "lodash";

import type { IGitRootAttr, IIPRootAttr, IURLRootAttr, Root } from "./types";

const getGitRootHost = (environmentUrl: string): string => {
  if (environmentUrl.endsWith("/")) {
    return environmentUrl;
  }

  return `${environmentUrl}/`;
};

const getIpRootHost = (root: IIPRootAttr): string =>
  root.port ? `${root.address}:${root.port}/` : `${root.address}/`;

const getUrlRootHost = (root: IURLRootAttr): string => {
  const urlRootWithPort = root.port
    ? `${root.protocol.toLowerCase()}://${root.host}:${root.port}${root.path}`
    : `${root.protocol.toLowerCase()}://${root.host}${root.path}`;

  return _.isNull(root.query)
    ? urlRootWithPort.endsWith("/")
      ? urlRootWithPort
      : `${urlRootWithPort}/`
    : `${urlRootWithPort}?${root.query}`;
};

const isGitRoot = (root: Root): root is IGitRootAttr =>
  root.__typename === "GitRoot";

const isIPRoot = (root: Root): root is IIPRootAttr =>
  root.__typename === "IPRoot";

const isURLRoot = (root: Root): root is IURLRootAttr =>
  root.__typename === "URLRoot";

export {
  isGitRoot,
  isIPRoot,
  isURLRoot,
  getGitRootHost,
  getIpRootHost,
  getUrlRootHost,
};
