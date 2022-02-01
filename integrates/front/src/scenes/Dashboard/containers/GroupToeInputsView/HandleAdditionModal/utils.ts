import type { IGitRootAttr, IIPRootAttr, IURLRootAttr, Root } from "./types";

const getGitRootHost = (environmentUrl: string): string => `${environmentUrl}/`;

const getIpRootHost = (root: IIPRootAttr): string =>
  root.port ? `${root.address}:${root.port}/` : `${root.address}/`;

const getUrlRootHost = (root: IURLRootAttr): string =>
  root.port
    ? `${root.protocol.toLowerCase()}://${root.host}:${root.port}/`
    : `${root.protocol.toLowerCase()}://${root.host}/`;

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
