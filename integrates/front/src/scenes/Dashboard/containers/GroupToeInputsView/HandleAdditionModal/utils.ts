import _ from "lodash";

import type { IGitRootAttr, IURLRootAttr, Root } from "./types";

const getGitRootHost = (environmentUrl: string): string => {
  if (environmentUrl.endsWith("/")) {
    return environmentUrl;
  }

  return `${environmentUrl}/`;
};

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

const isURLRoot = (root: Root): root is IURLRootAttr =>
  root.__typename === "URLRoot";

const isActiveGitRoot = (root: IGitRootAttr): boolean =>
  root.state === "ACTIVE";

const isActiveURLRoot = (root: IURLRootAttr): boolean =>
  root.state === "ACTIVE";

export {
  isActiveGitRoot,
  isActiveURLRoot,
  isGitRoot,
  isURLRoot,
  getGitRootHost,
  getUrlRootHost,
};
