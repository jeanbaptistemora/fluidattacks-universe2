import _ from "lodash";

import type { ICredentials } from "scenes/Dashboard/containers/Group-Content/GroupScopeView/types";
import type { AddGitRootResult } from "scenes/Dashboard/containers/Organization-Content/OrganizationWeakestView/types";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

type modalMessages = React.Dispatch<
  React.SetStateAction<{
    message: string;
    type: string;
  }>
>;

const getAreAllMutationValid = (results: AddGitRootResult[]): boolean[] => {
  return results.map((result: AddGitRootResult): boolean => {
    if (!_.isUndefined(result.data) && !_.isNull(result.data)) {
      const addGitRootSuccess: boolean = _.isUndefined(result.data.addGitRoot)
        ? true
        : result.data.addGitRoot.success;

      return addGitRootSuccess;
    }

    return false;
  });
};

const handleAddedError = (
  error: unknown,
  setModalMessages: modalMessages
): void => {
  switch (String(error).replace(/^Error: /u, "")) {
    case "Exception - Active root with the same Nickname already exists":
      setModalMessages({
        message: translate.t("group.scope.common.errors.duplicateNickname"),
        type: "error",
      });
      break;
    case "Exception - Root with the same URL/branch already exists":
      setModalMessages({
        message: translate.t("group.scope.common.errors.duplicateUrl"),
        type: "error",
      });
      break;
    case "Exception - Root name should not be included in the exception pattern":
      setModalMessages({
        message: translate.t("group.scope.git.errors.rootInGitignore"),
        type: "error",
      });
      break;
    case "Exception - Invalid characters":
      setModalMessages({
        message: translate.t("validations.invalidChar"),
        type: "error",
      });
      break;
    case "Exception - Unsanitized input found":
      setModalMessages({
        message: translate.t("validations.unsanitizedInputFound"),
        type: "error",
      });
      break;
    case "Exception - A credential exists with the same name":
      setModalMessages({
        message: translate.t("validations.invalidCredentialName"),
        type: "error",
      });
      break;
    case "Exception - Git repository was not accessible with given credentials":
      setModalMessages({
        message: translate.t("group.scope.git.errors.invalidGitCredentials"),
        type: "error",
      });
      break;
    case "Exception - Branch not found":
      setModalMessages({
        message: translate.t("group.scope.git.errors.invalidBranch"),
        type: "error",
      });
      break;
    case "Exception - Field cannot fill with blank characters":
      setModalMessages({
        message: translate.t("validations.invalidSpaceField"),
        type: "error",
      });
      break;
    case "Exception - The action is not allowed during the free trial":
      msgError(translate.t("group.scope.git.errors.trial"));
      break;
    default:
      setModalMessages({
        message: translate.t("groupAlerts.errorTextsad"),
        type: "error",
      });
      Logger.error("Couldn't add git roots", error);
  }
};

const getAddGitRootCredentialsVariables = (
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

export {
  getAreAllMutationValid,
  handleAddedError,
  getAddGitRootCredentialsVariables,
};
