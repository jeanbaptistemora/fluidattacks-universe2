/* eslint-disable react/forbid-prop-types */
import type { GraphQLError } from "graphql";
import _ from "lodash";
import type { BaseSchema, InferType } from "yup";
import { array, lazy, object, string } from "yup";
import type { TypedSchema } from "yup/lib/util/types";

import type { IAlertMessages, IRootAttr } from "./types";

import { Logger } from "utils/logger";
import { translate } from "utils/translations/translate";
import { regExps } from "utils/validations";

const { t } = translate;

const handleGroupCreateError = (
  graphQLErrors: readonly GraphQLError[],
  setMessages: IAlertMessages
): void => {
  graphQLErrors.forEach((error: GraphQLError): void => {
    switch (error.message) {
      case "Exception - Error invalid group name":
        setMessages({
          message: t("organization.tabs.groups.newGroup.invalidName"),
          type: "error",
        });
        break;
      case "Exception - User is not a member of the target organization":
        setMessages({
          message: t("organization.tabs.groups.newGroup.userNotInOrganization"),
          type: "error",
        });
        break;
      default:
        setMessages({
          message: t("groupAlerts.errorTextsad"),
          type: "error",
        });
        Logger.warning("An error occurred adding a group", error);
    }
  });
};

const handleRootCreateError = (
  graphQLErrors: readonly GraphQLError[],
  setMessages: IAlertMessages
): void => {
  graphQLErrors.forEach((error: GraphQLError): void => {
    switch (error.message) {
      case "Exception - Error empty value is not valid":
        setMessages({
          message: t("group.scope.git.errors.invalid"),
          type: "error",
        });
        break;
      case "Exception - Active root with the same Nickname already exists":
        setMessages({
          message: t("group.scope.common.errors.duplicateNickname"),
          type: "error",
        });
        break;
      case "Exception - Root with the same URL/branch already exists":
        setMessages({
          message: t("group.scope.common.errors.duplicateUrl"),
          type: "error",
        });
        break;
      case "Exception - Root name should not be included in the exception pattern":
        setMessages({
          message: t("group.scope.git.errors.rootInGitignore"),
          type: "error",
        });
        break;
      case "Exception - Invalid characters":
        setMessages({
          message: t("validations.invalidChar"),
          type: "error",
        });
        break;
      default:
        setMessages({
          message: t("groupAlerts.errorTextsad"),
          type: "error",
        });
        Logger.error("Couldn't add git roots", error);
    }
  });
};

const handleEnrollmentCreateError = (
  graphQLErrors: readonly GraphQLError[],
  setMessages: IAlertMessages
): void => {
  graphQLErrors.forEach((error: GraphQLError): void => {
    if (error.message === "Enrollment user already exists") {
      setMessages({
        message: t("autoenrollment.messages.error.enrollmentUser"),
        type: "error",
      });
    } else {
      setMessages({
        message: t("autoenrollment.messages.error.enrollment"),
        type: "error",
      });
      Logger.error("Couldn't add enrollment user data", error);
    }
  });
};

const handleValidationError = (
  graphQLErrors: readonly GraphQLError[],
  setMessages: IAlertMessages
): void => {
  graphQLErrors.forEach((error: GraphQLError): void => {
    switch (error.message) {
      case "Exception - Git repository was not accessible with given credentials":
        setMessages({
          message: t("group.scope.git.errors.invalidGitCredentials"),
          type: "error",
        });
        break;
      case "Exception - Branch not found":
        setMessages({
          message: t("group.scope.git.errors.invalidBranch"),
          type: "error",
        });
        break;
      default:
        setMessages({
          message: t("groupAlerts.errorTextsad"),
          type: "error",
        });
        Logger.error("Couldn't activate root", error);
    }
  });
};

const rootSchema = (isDirty: boolean): InferType<TypedSchema> =>
  lazy(
    (values: IRootAttr): BaseSchema =>
      object().shape({
        branch: string()
          .required(t("validations.required"))
          .matches(regExps.alphanumeric, t("validations.alphanumeric")),
        credentials: object({
          auth: string(),
          key: string()
            .when("type", {
              is: "SSH",
              otherwise: string(),
              then: string().required(t("validations.required")),
            })
            .test(
              "hasSshFormat",
              t("validations.invalidSshFormat"),
              (value): boolean => {
                const regex =
                  /^-{5}BEGIN OPENSSH PRIVATE KEY-{5}\n(?:[a-zA-Z0-9+/=]+\n)+-{5}END OPENSSH PRIVATE KEY-{5}\n?$/u;

                return (
                  value === undefined ||
                  values.credentials.type !== "SSH" ||
                  regex.test(value)
                );
              }
            ),
          name: string().when("type", {
            is: undefined,
            otherwise: string().required(t("validations.required")),
            then: string(),
          }),
          password: string()
            .when("type", {
              is: values.credentials.auth === "USER" ? "HTTPS" : "",
              otherwise: string(),
              then: string().required(t("validations.required")),
            })
            .test(
              "isGitAccesible",
              t("group.scope.git.repo.credentials.checkAccess.noAccess"),
              (value): boolean =>
                isDirty ||
                value === undefined ||
                values.credentials.type !== "HTTPS"
            ),
          token: string().when("type", {
            is: values.credentials.auth === "TOKEN" ? "HTTPS" : "",
            otherwise: string(),
            then: string().required(t("validations.required")),
          }),
          type: string().required(t("validations.required")),
          user: string()
            .when("type", {
              is: values.credentials.auth === "USER" ? "HTTPS" : "",
              otherwise: string(),
              then: string().required(t("validations.required")),
            })
            .test(
              "isGitAccesible",
              t("group.scope.git.repo.credentials.checkAccess.noAccess"),
              (value): boolean =>
                isDirty ||
                value === undefined ||
                values.credentials.type !== "HTTPS"
            ),
        }),
        env: string().required(t("validations.required")),
        exclusions: array().of(
          string()
            .required(t("validations.required"))
            .test(
              "excludeFormat",
              t("validations.excludeFormat"),
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
        url: string().required(t("validations.required")),
      })
  );

export {
  handleEnrollmentCreateError,
  handleGroupCreateError,
  handleRootCreateError,
  handleValidationError,
  rootSchema,
};
