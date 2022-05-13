import { Buffer } from "buffer";

import type { FetchResult } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";
import type { BaseSchema, InferType } from "yup";
import { array, boolean, lazy, object, string } from "yup";
import type { TypedSchema } from "yup/lib/util/types";

import type { IGitRootAttr } from "../types";
import { Alert } from "components/Alert";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

// GitModal helpers
interface IGitIgnoreAlertProps {
  gitignore: string[];
}

const GitIgnoreAlert: React.FC<IGitIgnoreAlertProps> = (
  props: IGitIgnoreAlertProps
): JSX.Element => {
  const { gitignore } = props;
  const { t } = useTranslation();

  if (_.isUndefined(gitignore)) {
    return <div />;
  }

  return _.isEmpty(gitignore) ? (
    <div />
  ) : (
    <Alert variant={"error"}>{t("group.scope.git.filter.warning")}</Alert>
  );
};

const gitModalSchema = (
  hasSquad: boolean,
  initialValues: IGitRootAttr,
  isCheckedHealthCheck: boolean,
  isDuplicated: (field: string) => boolean,
  nicknames: string[]
): InferType<TypedSchema> =>
  lazy(
    (values: IGitRootAttr): BaseSchema =>
      object().shape({
        branch: string().required(translate.t("validations.required")),
        environment: string().required(translate.t("validations.required")),
        gitignore: array().of(
          string()
            .required(translate.t("validations.required"))
            .test(
              "excludeFormat",
              translate.t("validations.excludeFormat"),
              (value): boolean => {
                const repoUrl = values.url;

                if (!_.isUndefined(repoUrl) && !_.isUndefined(value)) {
                  const [urlBasename] = repoUrl.split("/").slice(-1);
                  const repoName: string = urlBasename.endsWith(".git")
                    ? urlBasename.replace(".git", "")
                    : urlBasename;

                  return (
                    value
                      .toLowerCase()
                      .split("/")
                      .indexOf(repoName.toLowerCase()) !== 0
                  );
                }

                return false;
              }
            )
        ),
        healthCheckConfirm: array()
          .of(string())
          .test(
            "isChecked",
            translate.t("validations.required"),
            (): boolean => {
              const { healthCheckConfirm, includesHealthCheck } = values;
              if (!hasSquad || isCheckedHealthCheck) {
                return true;
              }
              if (
                includesHealthCheck !== null &&
                !includesHealthCheck &&
                healthCheckConfirm === undefined
              ) {
                return true;
              }
              if (healthCheckConfirm === undefined) {
                return false;
              }

              return (
                ((includesHealthCheck ?? false) &&
                  healthCheckConfirm.includes("includeA")) ||
                (!(includesHealthCheck ?? true) &&
                  healthCheckConfirm.includes("rejectA") &&
                  healthCheckConfirm.includes("rejectB") &&
                  healthCheckConfirm.includes("rejectC"))
              );
            }
          ),
        includesHealthCheck: boolean()
          .nullable()
          .when("$hasSquad", {
            is: (): boolean => hasSquad,
            otherwise: boolean().nullable(),
            then: boolean()
              .nullable()
              .required(translate.t("validations.required")),
          }),
        nickname: string()
          .when("url", {
            is: (url: string): boolean => isDuplicated(url),
            otherwise: string(),
            then: string().required(translate.t("validations.required")),
          })
          .matches(/^[a-zA-Z_0-9-]{1,128}$/u)
          .test(
            "isNickname",
            translate.t("validations.requireNickname"),
            (value): boolean =>
              !(
                nicknames.includes(value as string) &&
                initialValues.nickname !== value
              )
          ),
        url: string().required(translate.t("validations.required")),
      })
  );

// Index helpers

const handleCreationError = (
  graphQLErrors: readonly GraphQLError[],
  setModalMessages: React.Dispatch<
    React.SetStateAction<{
      message: string;
      type: string;
    }>
  >
): void => {
  graphQLErrors.forEach((error: GraphQLError): void => {
    switch (error.message) {
      case "Exception - Error empty value is not valid":
        setModalMessages({
          message: translate.t("group.scope.git.errors.invalid"),
          type: "error",
        });
        break;
      case "Exception - Active root with the same Nickname already exists":
        setModalMessages({
          message: translate.t("group.scope.common.errors.duplicateNickname"),
          type: "error",
        });
        break;
      case "Exception - Active root with the same URL/branch already exists":
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
      default:
        setModalMessages({
          message: translate.t("groupAlerts.errorTextsad"),
          type: "error",
        });
        Logger.error("Couldn't add git roots", error);
    }
  });
};

const handleUpdateError = (
  graphQLErrors: readonly GraphQLError[],
  setModalMessages: React.Dispatch<
    React.SetStateAction<{
      message: string;
      type: string;
    }>
  >,
  scope: "envs" | "root" | "tours"
): void => {
  graphQLErrors.forEach((error: GraphQLError): void => {
    const showMessage = (translation: string): void => {
      if (scope === "root") {
        setModalMessages({
          message: translate.t(translation),
          type: "error",
        });
      } else {
        msgError(translate.t(translation));
      }
    };
    switch (error.message) {
      case "Exception - Error empty value is not valid":
        showMessage("group.scope.git.errors.invalid");
        break;
      case "Exception - A root with reported vulns can't be updated":
        showMessage("group.scope.common.errors.hasVulns");
        break;
      case "Exception - Active root with the same URL/branch already exists":
        showMessage("group.scope.common.errors.duplicateUrl");
        break;
      case "Exception - Invalid characters":
        showMessage("validations.invalidChar");
        break;
      case "Exception - Git repository was not accessible with given credentials":
        showMessage("group.scope.git.errors.invalidGitCredentials");
        break;
      default:
        showMessage("groupAlerts.errorTextsad");
        Logger.error(`Couldn't update git ${scope}`, error);
    }
  });
};

const handleActivationError = (
  graphQLErrors: readonly GraphQLError[]
): void => {
  graphQLErrors.forEach((error: GraphQLError): void => {
    if (
      error.message ===
      "Exception - Active root with the same URL/branch already exists"
    ) {
      msgError(translate.t("group.scope.common.errors.duplicateUrl"));
    } else {
      msgError(translate.t("groupAlerts.errorTextsad"));
      Logger.error("Couldn't activate root", error);
    }
  });
};

const handleSyncError = (graphQLErrors: readonly GraphQLError[]): void => {
  graphQLErrors.forEach((error: GraphQLError): void => {
    switch (error.message) {
      case "Exception - Access denied or credential not found":
        msgError(translate.t("group.scope.git.sync.noCredentials"));
        break;
      case "Exception - The root already has an active cloning process":
        msgError(translate.t("group.scope.git.sync.alreadyCloning"));
        break;
      default:
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.error("Couldn't queue root cloning", error);
    }
  });
};

const hasCheckedItem = (
  checkedItems: Record<string, boolean>,
  columnName: string
): boolean => {
  return (
    Object.values(checkedItems).filter((val: boolean): boolean => val)
      .length === 1 && checkedItems[columnName]
  );
};

function useGitSubmit(
  addGitRoot: (
    variables: Record<string, unknown>
  ) => Promise<FetchResult<unknown>>,
  groupName: string,
  isManagingRoot: false | { mode: "ADD" | "EDIT" },
  updateGitRoot: (
    variables: Record<string, unknown>
  ) => Promise<FetchResult<unknown>>
): ({
  branch,
  credentials,
  environment,
  gitignore,
  id,
  includesHealthCheck,
  nickname,
  url,
  useVpn,
}: IGitRootAttr) => Promise<void> {
  return useCallback(
    async ({
      branch,
      credentials,
      environment,
      gitignore,
      id,
      includesHealthCheck,
      nickname,
      url,
      useVpn,
    }: IGitRootAttr): Promise<void> => {
      if (isManagingRoot !== false) {
        if (isManagingRoot.mode === "ADD") {
          mixpanel.track("AddGitRoot");
          await addGitRoot({
            variables: {
              branch: branch.trim(),
              credentials:
                credentials.key === "" &&
                credentials.user === "" &&
                credentials.password === "" &&
                credentials.id === "" &&
                credentials.token === ""
                  ? null
                  : {
                      id: credentials.id,
                      key:
                        credentials.key === ""
                          ? undefined
                          : Buffer.from(credentials.key).toString("base64"),
                      name: credentials.name,
                      password: credentials.password,
                      token: credentials.token,
                      type: credentials.type,
                      user: credentials.user,
                    },
              environment,
              gitignore,
              groupName,
              includesHealthCheck: includesHealthCheck ?? false,
              nickname,
              url: url.trim(),
              useVpn,
            },
          });
        } else {
          mixpanel.track("EditGitRoot");
          await updateGitRoot({
            variables: {
              branch,
              credentials:
                _.isUndefined(credentials.key) &&
                _.isUndefined(credentials.user) &&
                _.isUndefined(credentials.password) &&
                _.isUndefined(credentials.token)
                  ? !_.isUndefined(credentials.id) && credentials.id !== ""
                    ? {
                        id: credentials.id,
                        name: credentials.name,
                        type: credentials.type,
                      }
                    : undefined
                  : {
                      key:
                        credentials.key === "" || _.isUndefined(credentials.key)
                          ? undefined
                          : Buffer.from(credentials.key).toString("base64"),
                      name: credentials.name,
                      password: credentials.password,
                      token: credentials.token,
                      type: credentials.type,
                      user: credentials.user,
                    },
              environment,
              gitignore,
              groupName,
              id,
              includesHealthCheck,
              url,
              useVpn,
            },
          });
        }
      }
    },
    [addGitRoot, groupName, isManagingRoot, updateGitRoot]
  );
}

function filterSelectStatus(
  rows: IGitRootAttr[],
  currentValue: string
): IGitRootAttr[] {
  return rows.filter((row: IGitRootAttr): boolean =>
    _.isEmpty(currentValue) ? true : row.cloningStatus.status === currentValue
  );
}

function filterSelectIncludesHealthCheck(
  rows: IGitRootAttr[],
  currentValue: string
): IGitRootAttr[] {
  const isHealthCheckIncluded = currentValue === "true";

  return rows.filter((row: IGitRootAttr): boolean =>
    _.isEmpty(currentValue)
      ? true
      : row.includesHealthCheck === isHealthCheckIncluded
  );
}

export {
  filterSelectStatus,
  filterSelectIncludesHealthCheck,
  GitIgnoreAlert,
  gitModalSchema,
  handleCreationError,
  handleUpdateError,
  handleActivationError,
  handleSyncError,
  hasCheckedItem,
  useGitSubmit,
};
