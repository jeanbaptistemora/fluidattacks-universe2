import type { IGitRootAttr, IIPRootAttr, IURLRootAttr, Root } from "./types";

const isGitRoot = (root: Root): root is IGitRootAttr =>
  root.__typename === "GitRoot";

const isIPRoot = (root: Root): root is IIPRootAttr =>
  root.__typename === "IPRoot";

const isURLRoot = (root: Root): root is IURLRootAttr =>
  root.__typename === "URLRoot";

export { isGitRoot, isIPRoot, isURLRoot };
