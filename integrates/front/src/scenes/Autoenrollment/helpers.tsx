/* eslint-disable react/forbid-prop-types */
import type { GraphQLError } from "graphql";
import type { BaseSchema, InferType } from "yup";
import { array, lazy, object, string } from "yup";
import type { TypedSchema } from "yup/lib/util/types";

import type { IAlertMessages, IRootAttr } from "./types";

import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

const handleGroupCreateError = (
  graphQLErrors: readonly GraphQLError[]
): void => {
  graphQLErrors.forEach((error: GraphQLError): void => {
    switch (error.message) {
      case "Exception - Error invalid group name":
        msgError(translate.t("organization.tabs.groups.newGroup.invalidName"));
        break;
      case "Exception - User is not a member of the target organization":
        msgError(
          translate.t("organization.tabs.groups.newGroup.userNotInOrganization")
        );
        break;
      default:
        msgError(translate.t("groupAlerts.errorTextsad"));
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
          message: translate.t("group.scope.git.errors.invalid"),
          type: "error",
        });
        break;
      case "Exception - Active root with the same Nickname already exists":
        setMessages({
          message: translate.t("group.scope.common.errors.duplicateNickname"),
          type: "error",
        });
        break;
      case "Exception - Active root with the same URL/branch already exists":
        setMessages({
          message: translate.t("group.scope.common.errors.duplicateUrl"),
          type: "error",
        });
        break;
      case "Exception - Root name should not be included in the exception pattern":
        setMessages({
          message: translate.t("group.scope.git.errors.rootInGitignore"),
          type: "error",
        });
        break;
      case "Exception - Invalid characters":
        setMessages({
          message: translate.t("validations.invalidChar"),
          type: "error",
        });
        break;
      default:
        setMessages({
          message: translate.t("groupAlerts.errorTextsad"),
          type: "error",
        });
        Logger.error("Couldn't add git roots", error);
    }
  });
};

const handleValidationError = (
  graphQLErrors: readonly GraphQLError[],
  setMessages: IAlertMessages
): void => {
  graphQLErrors.forEach((error: GraphQLError): void => {
    if (
      error.message ===
      "Exception - Git repository was not accessible with given credentials"
    ) {
      setMessages({
        message: translate.t("group.scope.git.errors.invalidGitCredentials"),
        type: "error",
      });
    } else {
      setMessages({
        message: translate.t("groupAlerts.errorTextsad"),
        type: "error",
      });
      Logger.error("Couldn't activate root", error);
    }
  });
};

const rootSchema = (isGitAccessible: boolean): InferType<TypedSchema> =>
  lazy(
    (values: IRootAttr): BaseSchema =>
      object().shape({
        branch: string().required(translate.t("validations.required")),
        credentials: object({
          auth: string(),
          key: string()
            .when("type", {
              is: "SSH",
              otherwise: string(),
              then: string().required(translate.t("validations.required")),
            })
            .test(
              "hasSshFormat",
              translate.t("validations.invalidSshFormat"),
              (value): boolean => {
                const regex =
                  /^-{5}BEGIN OPENSSH PRIVATE KEY-{5}\n(?:[a-zA-Z0-9+/=]+\n)+-{5}END OPENSSH PRIVATE KEY-{5}\n?$/u;

                if (value === undefined || values.credentials.type !== "SSH") {
                  return true;
                }

                return regex.test(value);
              }
            )
            .test(
              "isGitAccesible",
              translate.t(
                "group.scope.git.repo.credentials.checkAccess.noAccess"
              ),
              (value): boolean => {
                if (value === undefined || values.credentials.type !== "SSH") {
                  return true;
                }

                return isGitAccessible;
              }
            ),
          name: string().when("type", {
            is: undefined,
            otherwise: string().required(translate.t("validations.required")),
            then: string(),
          }),
          password: string()
            .when("type", {
              is: values.credentials.auth === "USER" ? "HTTPS" : "",
              otherwise: string(),
              then: string().required(translate.t("validations.required")),
            })
            .test(
              "isGitAccesible",
              translate.t(
                "group.scope.git.repo.credentials.checkAccess.noAccess"
              ),
              (value): boolean => {
                if (
                  value === undefined ||
                  values.credentials.type !== "HTTPS"
                ) {
                  return true;
                }

                return isGitAccessible;
              }
            ),
          token: string()
            .when("type", {
              is: values.credentials.auth === "TOKEN" ? "HTTPS" : "",
              otherwise: string(),
              then: string().required(translate.t("validations.required")),
            })
            .test(
              "isGitAccesible",
              translate.t(
                "group.scope.git.repo.credentials.checkAccess.noAccess"
              ),
              (value): boolean => {
                if (
                  value === undefined ||
                  values.credentials.type !== "HTTPS"
                ) {
                  return true;
                }

                return isGitAccessible;
              }
            ),
          type: string().required(translate.t("validations.required")),
          user: string()
            .when("type", {
              is: values.credentials.auth === "USER" ? "HTTPS" : "",
              otherwise: string(),
              then: string().required(translate.t("validations.required")),
            })
            .test(
              "isGitAccesible",
              translate.t(
                "group.scope.git.repo.credentials.checkAccess.noAccess"
              ),
              (value): boolean => {
                if (
                  value === undefined ||
                  values.credentials.type !== "HTTPS"
                ) {
                  return true;
                }

                return isGitAccessible;
              }
            ),
        }),
        env: string().required(translate.t("validations.required")),
        exclusions: array().of(string()),
        url: string().required(translate.t("validations.required")),
      })
  );

export {
  handleGroupCreateError,
  handleRootCreateError,
  handleValidationError,
  rootSchema,
};
