/* eslint-disable react/forbid-prop-types */
import type { FetchResult } from "@apollo/client";
import type { GraphQLError } from "graphql";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import { useCallback } from "react";
import type { BaseSchema, InferType } from "yup";
import { array, lazy, object, string } from "yup";
import type { TypedSchema } from "yup/lib/util/types";

import { Logger } from "utils/logger";
import { translate } from "utils/translations/translate";

type modalMessages = React.Dispatch<
  React.SetStateAction<{
    message: string;
    type: string;
  }>
>;

interface IRootAttr {
  branch: string;
  credentials: {
    auth: "TOKEN" | "USER";
    id: string;
    key: string;
    name: string;
    password: string;
    token: string;
    type: "" | "HTTPS" | "SSH";
    user: string;
  };
  env: string;
  exclusions: string[];
  url: string;
}

const handleCreationError = (
  graphQLErrors: readonly GraphQLError[],
  setMessages: modalMessages
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
  setMessages: modalMessages
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

function useRootSubmit(
  addGitRoot: (
    variables: Record<string, unknown>
  ) => Promise<FetchResult<unknown>>,
  group: string
): ({ branch, credentials, env, exclusions, url }: IRootAttr) => Promise<void> {
  return useCallback(
    async ({
      branch,
      credentials,
      env,
      exclusions,
      url,
    }: IRootAttr): Promise<void> => {
      mixpanel.track("AddGitRoot");
      await addGitRoot({
        variables: {
          branch: branch.trim(),
          credentials: {
            id: "",
            key: credentials.key,
            name: credentials.name,
            password: credentials.password,
            token: credentials.token,
            type: credentials.type,
            user: credentials.user,
          },
          environment: env,
          gitignore: exclusions,
          groupName: group,
          includesHealthCheck: false,
          nickname: "",
          url: url.trim(),
          useVpn: false,
        },
      });
    },
    [addGitRoot, group]
  );
}

const rootSchema = (isGitAccessible: boolean): InferType<TypedSchema> =>
  lazy(
    (values: IRootAttr): BaseSchema =>
      object().shape({
        branch: string().required(),
        credentials: object({
          auth: string(),
          id: string(),
          key: string()
            .when("type", {
              is: (type: string): boolean => {
                return type === "SSH";
              },
              otherwise: string(),
              then: string().required(translate.t("validations.required")),
            })
            .test(
              "isGitAccesible",
              translate.t(
                "group.scope.git.repo.credentials.checkAccess.noAccess"
              ),
              (): boolean => {
                return isGitAccessible;
              }
            )
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
            ),
          name: string().when("type", {
            is: undefined,
            otherwise: string().required(translate.t("validations.required")),
            then: string(),
          }),
          password: string()
            .when("type", {
              is: (type: string): boolean => {
                return type === "HTTPS" && values.credentials.auth === "USER";
              },
              otherwise: string(),
              then: string().required(translate.t("validations.required")),
            })
            .test(
              "isGitAccesible",
              translate.t(
                "group.scope.git.repo.credentials.checkAccess.noAccess"
              ),
              (): boolean => {
                return isGitAccessible;
              }
            ),
          token: string()
            .when("type", {
              is: (type: string): boolean => {
                return type === "HTTPS" && values.credentials.auth === "TOKEN";
              },
              otherwise: string(),
              then: string().required(translate.t("validations.required")),
            })
            .test(
              "isGitAccesible",
              translate.t(
                "group.scope.git.repo.credentials.checkAccess.noAccess"
              ),
              (): boolean => {
                return isGitAccessible;
              }
            ),
          type: string(),
          user: string()
            .when("type", {
              is: (type: string): boolean => {
                return type === "HTTPS" && values.credentials.auth === "USER";
              },
              otherwise: string(),
              then: string().required(translate.t("validations.required")),
            })
            .test(
              "isGitAccesible",
              translate.t(
                "group.scope.git.repo.credentials.checkAccess.noAccess"
              ),
              (): boolean => {
                return isGitAccessible;
              }
            ),
        }),
        environment: string().required(),
        exclusions: array().of(string()),
        url: string().required(),
      })
  );

export type { IRootAttr };

export {
  handleCreationError,
  handleValidationError,
  rootSchema,
  useRootSubmit,
};
