import type {
  ICredentialsAttr,
  IGitRootAttr,
  IIPRootAttr,
  IURLRootAttr,
  Root,
} from "./types";

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

const formatAuthCredentials = (value: ICredentialsAttr): "TOKEN" | "USER" => {
  if (value.isToken) {
    return "TOKEN";
  }

  return "USER";
};
const formatTypeCredentials = (
  value: ICredentialsAttr
): "SSH" | "TOKEN" | "USER" => {
  if (value.type === "HTTPS") {
    return formatAuthCredentials(value);
  }

  return "SSH";
};

export {
  isGitRoot,
  isIPRoot,
  isURLRoot,
  mapInactiveStatus,
  formatAuthCredentials,
  formatTypeCredentials,
};
