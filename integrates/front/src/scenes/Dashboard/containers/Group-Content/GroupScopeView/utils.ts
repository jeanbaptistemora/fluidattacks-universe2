import _ from "lodash";

import type {
  ICredentials,
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
): "OAUTH" | "SSH" | "TOKEN" | "USER" => {
  if (value.type === "HTTPS") {
    return formatAuthCredentials(value);
  }

  if (value.type === "OAUTH") {
    return "OAUTH";
  }

  return "SSH";
};

const getAddGitRootCredentials = (
  credentials: ICredentials
): Record<string, boolean | string | undefined> | undefined => {
  if (_.isEmpty(credentials.id)) {
    if (
      _.isEmpty(credentials.key) &&
      _.isEmpty(credentials.user) &&
      _.isEmpty(credentials.password) &&
      _.isEmpty(credentials.token)
    ) {
      return undefined;
    }

    return {
      azureOrganization:
        _.isUndefined(credentials.azureOrganization) ||
        _.isUndefined(credentials.isPat) ||
        !credentials.isPat
          ? undefined
          : credentials.azureOrganization,
      isPat: _.isUndefined(credentials.isPat) ? false : credentials.isPat,
      key: _.isEmpty(credentials.key)
        ? undefined
        : Buffer.from(credentials.key).toString("base64"),
      name: credentials.name,
      password: credentials.password,
      token: credentials.token,
      type: credentials.type,
      user: credentials.user,
    };
  }

  return {
    id: credentials.id,
  };
};

const getUpdateGitRootCredentials = (
  credentials: ICredentials
): Record<string, boolean | string | undefined> | undefined => {
  if (_.isEmpty(credentials.id)) {
    if (
      _.isEmpty(credentials.key) &&
      _.isEmpty(credentials.user) &&
      _.isEmpty(credentials.password) &&
      _.isEmpty(credentials.token)
    ) {
      return undefined;
    }

    return {
      key: _.isEmpty(credentials.key)
        ? undefined
        : Buffer.from(credentials.key).toString("base64"),
      name: credentials.name,
      password: credentials.password,
      token: credentials.token,
      type: credentials.type,
      user: credentials.user,
    };
  }

  return {
    id: credentials.id,
  };
};

export {
  isGitRoot,
  isIPRoot,
  isURLRoot,
  mapInactiveStatus,
  formatAuthCredentials,
  formatTypeCredentials,
  getAddGitRootCredentials,
  getUpdateGitRootCredentials,
};
