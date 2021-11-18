import type { FetchResult } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import { track } from "mixpanel-browser";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";
import type { BaseSchema } from "yup";
import { array, lazy, object, string } from "yup";

import type { IGitRootAttr } from "../types";
import { Alert } from "styles/styledComponents";
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
    <Alert>{t("group.scope.git.filter.warning")}</Alert>
  );
};

const gitModalSchema = lazy(
  (values: IGitRootAttr): BaseSchema =>
    object().shape({
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
      nickname: string().matches(/^[a-zA-Z_0-9-]{1,128}$/u),
      url: string().required(translate.t("validations.required")),
    })
);

// Index helpers

const handleCreationError = (graphQLErrors: readonly GraphQLError[]): void => {
  graphQLErrors.forEach((error: GraphQLError): void => {
    switch (error.message) {
      case "Exception - Error empty value is not valid":
        msgError(translate.t("group.scope.git.errors.invalid"));
        break;
      case "Exception - Active root with the same Nickname already exists":
        msgError(translate.t("group.scope.common.errors.duplicateNickname"));
        break;
      case "Exception - Active root with the same URL/branch already exists":
        msgError(translate.t("group.scope.common.errors.duplicateUrl"));
        break;
      case "Exception - Root name should not be included in the exception pattern":
        msgError(translate.t("group.scope.git.errors.rootInGitignore"));
        break;
      case "Exception - Invalid characters":
        msgError(translate.t("validations.invalidChar"));
        break;
      default:
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.error("Couldn't add git roots", error);
    }
  });
};

const handleUpdateError = (
  graphQLErrors: readonly GraphQLError[],
  scope: "envs" | "root"
): void => {
  graphQLErrors.forEach((error: GraphQLError): void => {
    switch (error.message) {
      case "Exception - Error empty value is not valid":
        msgError(translate.t("group.scope.git.errors.invalid"));
        break;
      case "Exception - A root with reported vulns can't be updated":
        msgError(translate.t("group.scope.common.errors.hasVulns"));
        break;
      case "Exception - Active root with the same URL/branch already exists":
        msgError(translate.t("group.scope.common.errors.duplicateUrl"));
        break;
      case "Exception - Invalid characters":
        msgError(translate.t("validations.invalidChar"));
        break;
      default:
        msgError(translate.t("groupAlerts.errorTextsad"));
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
  environment,
  gitignore,
  id,
  includesHealthCheck,
  nickname,
  url,
}: IGitRootAttr) => Promise<void> {
  return useCallback(
    async ({
      branch,
      environment,
      gitignore,
      id,
      includesHealthCheck,
      nickname,
      url,
    }: IGitRootAttr): Promise<void> => {
      if (isManagingRoot !== false) {
        if (isManagingRoot.mode === "ADD") {
          track("AddGitRoot");
          await addGitRoot({
            variables: {
              branch: branch.trim(),
              environment,
              gitignore,
              groupName,
              includesHealthCheck,
              nickname,
              url: url.trim(),
            },
          });
        } else {
          track("EditGitRoot");
          await updateGitRoot({
            variables: {
              branch,
              environment,
              gitignore,
              groupName,
              id,
              includesHealthCheck,
              url,
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

export {
  filterSelectStatus,
  GitIgnoreAlert,
  gitModalSchema,
  handleCreationError,
  handleUpdateError,
  handleActivationError,
  hasCheckedItem,
  useGitSubmit,
};
