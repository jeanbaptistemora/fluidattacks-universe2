import type { IIPRootAttr, Root } from "./types";

const isIPRoot = (root: Root): root is IIPRootAttr =>
  root.__typename === "IPRoot";

const isActiveIPRoot = (root: IIPRootAttr): boolean => root.state === "ACTIVE";

export { isIPRoot, isActiveIPRoot };
