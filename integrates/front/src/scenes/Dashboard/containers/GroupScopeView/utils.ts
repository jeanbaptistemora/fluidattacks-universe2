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
